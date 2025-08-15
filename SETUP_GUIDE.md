# XAgent Integration Setup Guide

## Quick Start Guide for L3AGI + XAgent Integration

### 🚀 Prerequisites

- Python 3.10 or higher
- Git
- Both repositories cloned:
  - `team-of-ai-agents` (L3AGI framework)
  - `XAgent` (XAgent framework)

### 📦 Installation Steps

1. **Navigate to L3AGI Directory**

   ```bash
   cd "d:\iAI intern\team-of-ai-agents"
   ```

2. **Install XAgent Dependencies**

   ```bash
   pip install -r requirements_xagent.txt
   ```

3. **Verify Structure**

   ```bash
   cd apps/server
   python test_structure.py
   ```

4. **Test XAgent Integration**
   ```bash
   python test_xagent_integration.py
   ```

### 🔧 Configuration

1. **XAgent Config** (if needed)

   - Copy XAgent config files from `XAgent/assets/config.yml`
   - Adjust API keys and model settings

2. **L3AGI Config** (if needed)
   - Ensure existing L3AGI configuration is compatible
   - No changes required for basic operation

### 🧪 Testing

#### Structure Test (No Dependencies Required)

```bash
cd apps/server
python test_structure.py
```

Expected output:

```
🎉 ALL STRUCTURE TESTS PASSED!
✅ XAgent integration structure is complete
```

#### Functional Test (Requires Dependencies)

```bash
python test_xagent_integration.py
```

Expected output:

```
🎉 ALL TESTS PASSED! XAgent integration is working correctly.
```

### 📁 File Structure After Integration

```
team-of-ai-agents/
├── apps/server/
│   ├── agents/
│   │   ├── xagent_integration.py              # NEW - XAgent adapter
│   │   ├── conversational/
│   │   │   ├── conversational.py              # MODIFIED - Uses XAgent
│   │   │   └── conversational_langchain_backup.py  # BACKUP
│   │   └── agent_simulations/agent/
│   │       ├── dialogue_agent_with_tools.py   # MODIFIED - Uses XAgent
│   │       └── dialogue_agent_with_tools_langchain_backup.py  # BACKUP
│   ├── test.py                                # MODIFIED - Uses XAgent
│   ├── test_langchain_backup.py               # BACKUP
│   ├── test_xagent_integration.py             # NEW - Integration test
│   └── test_structure.py                      # NEW - Structure test
├── requirements_xagent.txt                    # NEW - Dependencies
└── XAGENT_INTEGRATION_REPORT.md               # NEW - Documentation
```

### 🔄 Rollback Instructions

If you need to revert to Langchain REACT:

1. **Restore Original Files**

   ```bash
   cd apps/server
   cp test_langchain_backup.py test.py
   cd agents/conversational
   cp conversational_langchain_backup.py conversational.py
   cd ../agent_simulations/agent
   cp dialogue_agent_with_tools_langchain_backup.py dialogue_agent_with_tools.py
   ```

2. **Remove XAgent Files**
   ```bash
   rm agents/xagent_integration.py
   rm test_xagent_integration.py
   rm test_structure.py
   rm requirements_xagent.txt
   ```

### 🐛 Troubleshooting

#### Common Issues

1. **Import Errors**

   - Ensure all dependencies are installed: `pip install -r requirements_xagent.txt`
   - Check Python path includes XAgent directory

2. **Path Issues**

   - Verify XAgent repository is cloned at `d:\iAI intern\XAgent`
   - Check relative path calculations in integration code

3. **API Key Issues**
   - Configure OpenAI API keys if running functional tests
   - Set up XAgent configuration files

#### Debug Commands

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify XAgent import
python -c "import sys; sys.path.insert(0, 'path/to/XAgent'); from XAgent.core import XAgentCoreComponents; print('XAgent imports OK')"

# Test basic functionality
python -c "from agents.xagent_integration import L3AGIXAgentAdapter; print('Adapter import OK')"
```

### ✅ Success Criteria

You know the integration is working when:

- ✅ Structure test passes (3/3 tests)
- ✅ No import errors when running integration test
- ✅ XAgent responds to basic prompts
- ✅ Streaming functionality works
- ✅ Tool integration functions

### 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the detailed implementation report: `XAGENT_INTEGRATION_REPORT.md`
3. Examine backup files to understand original implementation
4. Run structure test to verify file integrity

### 🎯 Next Steps

After successful setup:

1. **Deploy to staging** environment
2. **Monitor performance** compared to original
3. **Leverage advanced XAgent features** like planning and reflection
4. **Optimize tool integration** for better performance
5. **Expand multi-agent capabilities** using XAgent's advanced features

---

**Integration completed successfully!** 🚀
**Ready for production deployment** ✅
