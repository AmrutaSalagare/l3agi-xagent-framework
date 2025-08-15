"""
XAgent Integration Module for L3AGI Framework

This module provides a compatibility layer between XAgent and L3AGI's existing interfaces.
It allows seamless integration of XAgent's autonomous capabilities while maintaining
compatibility with the current L3AGI agent system.
"""

import asyncio
import os
import sys
from typing import List, Dict, Any, Optional
from uuid import uuid4

# Add XAgent to the Python path
xagent_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'XAgent')
sys.path.insert(0, xagent_path)

from XAgent.core import XAgentCoreComponents, XAgentParam
from XAgent.agent.tool_agent import ToolAgent
from XAgent.workflow.base_query import AutoGPTQuery
from XAgent.message_history import Message
from XAgent.config import CONFIG, ARGS
from XAgent.function_handler import FunctionHandler
from XAgent.toolserver_interface import ToolServerInterface
from XAgent.logs import logger


class L3AGIXAgentAdapter:
    """
    Adapter class to integrate XAgent into L3AGI framework
    Provides compatibility with existing L3AGI agent interfaces
    """
    
    def __init__(self, config=None, tools=None, system_message="", memory=None):
        """
        Initialize the XAgent adapter
        
        Args:
            config: L3AGI configuration object
            tools: List of L3AGI tools
            system_message: System message for the agent
            memory: Memory object (ZepMemory or similar)
        """
        self.config = config
        self.tools = tools or []
        self.system_message = system_message
        self.memory = memory
        self.session_id = str(uuid4())
        
        # Initialize XAgent components
        self.xagent_components = None
        self.tool_agent = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize XAgent components"""
        if self.is_initialized:
            return
            
        try:
            # Create XAgent parameter object
            query_data = {
                "task": self.system_message,
                "upload_files": [],
                "role": "Assistant",
                "mode": "auto"
            }
            
            xagent_param = XAgentParam(
                config=self._convert_config(),
                query=AutoGPTQuery(**query_data),
                newly_created=True
            )
            
            # Initialize core components (simplified for integration)
            self.xagent_components = XAgentCoreComponents()
            
            # Create mock interaction object for initialization
            from types import SimpleNamespace
            mock_interaction = SimpleNamespace()
            mock_interaction.base = SimpleNamespace()
            mock_interaction.base.interaction_id = self.session_id
            mock_interaction.logger = logger
            
            # Initialize tool agent
            self.tool_agent = ToolAgent(
                config=xagent_param.config,
                prompt_messages=self._create_prompt_messages()
            )
            
            self.is_initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize XAgent: {e}")
            raise
    
    def _convert_config(self):
        """Convert L3AGI config to XAgent format"""
        # Basic XAgent configuration
        xagent_config = {
            "default_completion_kwargs": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "enable_ask_human_for_help": False,
            "max_retry_times": 3
        }
        
        # Override with L3AGI config if available
        if self.config:
            if hasattr(self.config, 'model_name'):
                xagent_config["default_completion_kwargs"]["model"] = self.config.model_name
            if hasattr(self.config, 'temperature'):
                xagent_config["default_completion_kwargs"]["temperature"] = self.config.temperature
                
        return xagent_config
    
    def _create_prompt_messages(self) -> List[Message]:
        """Create XAgent prompt messages from system message"""
        messages = []
        if self.system_message:
            messages.append(Message(
                role="system",
                content=self.system_message
            ))
        return messages
    
    def _convert_tools_to_xagent_format(self) -> List[Dict]:
        """Convert L3AGI tools to XAgent function format"""
        xagent_functions = []
        
        for tool in self.tools:
            function_schema = {
                "name": getattr(tool, 'name', tool.__class__.__name__),
                "description": getattr(tool, 'description', ''),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
            
            # Add tool-specific parameters if available
            if hasattr(tool, 'args_schema'):
                schema = tool.args_schema
                if hasattr(schema, '__fields__'):
                    for field_name, field in schema.__fields__.items():
                        function_schema["parameters"]["properties"][field_name] = {
                            "type": self._get_json_type(field.type_),
                            "description": field.field_info.description or ""
                        }
                        if field.required:
                            function_schema["parameters"]["required"].append(field_name)
            
            xagent_functions.append(function_schema)
        
        return xagent_functions
    
    def _get_json_type(self, python_type) -> str:
        """Convert Python type to JSON schema type"""
        type_mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }
        return type_mapping.get(python_type, "string")
    
    async def arun(self, prompt: str) -> str:
        """
        Async run method to execute a prompt with XAgent
        
        Args:
            prompt: User input prompt
            
        Returns:
            Agent response string
        """
        await self.initialize()
        
        try:
            # Convert tools to XAgent format
            functions = self._convert_tools_to_xagent_format()
            
            # Create additional messages for the prompt
            additional_messages = [Message(role="user", content=prompt)]
            
            # Use XAgent's ToolAgent to process the request
            placeholders = {
                "system": {
                    "task": prompt,
                    "tools": str(functions)
                }
            }
            
            response, tokens = self.tool_agent.parse(
                placeholders=placeholders,
                functions=functions,
                additional_messages=additional_messages
            )
            
            # Extract the response content
            if isinstance(response, dict):
                if 'content' in response:
                    return response['content']
                elif 'function_call' in response:
                    # Handle function call responses
                    return self._handle_function_call(response['function_call'])
                else:
                    return str(response)
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"XAgent execution failed: {e}")
            return f"Error: {str(e)}"
    
    def run(self, prompt: str) -> str:
        """
        Synchronous run method (wrapper around async version)
        
        Args:
            prompt: User input prompt
            
        Returns:
            Agent response string
        """
        try:
            # Run async method in event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If already in an event loop, create a new task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.arun(prompt))
                    return future.result()
            else:
                return loop.run_until_complete(self.arun(prompt))
        except Exception as e:
            logger.error(f"XAgent sync execution failed: {e}")
            return f"Error: {str(e)}"
    
    def _handle_function_call(self, function_call: Dict) -> str:
        """Handle function call execution"""
        function_name = function_call.get('name', '')
        arguments = function_call.get('arguments', {})
        
        # Find and execute the corresponding tool
        for tool in self.tools:
            tool_name = getattr(tool, 'name', tool.__class__.__name__)
            if tool_name == function_name:
                try:
                    if hasattr(tool, 'run'):
                        result = tool.run(**arguments)
                    elif hasattr(tool, '__call__'):
                        result = tool(**arguments)
                    else:
                        result = f"Tool {function_name} is not callable"
                    
                    return str(result)
                except Exception as e:
                    return f"Error executing tool {function_name}: {str(e)}"
        
        return f"Tool {function_name} not found"
    
    async def astream(self, prompt: str):
        """
        Async streaming method for XAgent responses
        
        Args:
            prompt: User input prompt
            
        Yields:
            Response chunks
        """
        response = await self.arun(prompt)
        
        # Simple streaming simulation - split response into chunks
        words = response.split()
        for i, word in enumerate(words):
            if i < len(words) - 1:
                yield word + " "
            else:
                yield word


class XAgentStreamingResponse:
    """
    Streaming response wrapper for XAgent
    """
    
    def __init__(self, adapter: L3AGIXAgentAdapter, prompt: str):
        self.adapter = adapter
        self.prompt = prompt
        
    def __aiter__(self):
        return self.adapter.astream(self.prompt)
