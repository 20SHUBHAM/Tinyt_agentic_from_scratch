# ⚡ Quick Start Guide

Get your Agentic AI Focus Group Workflow running in minutes!

## 🎯 Option 1: Replit (Fastest - 5 minutes)

1. **Go to Replit**: [replit.com](https://replit.com)
2. **Import**: Click "Create Repl" → "Import from GitHub" → Paste this repo URL
3. **Set Secrets**: 
   - Click Secrets tab (🔒)
   - Add: `OPENAI_API_KEY = your_openai_key_here`
4. **Run**: Click the "Run" button
5. **Done!** Access your live app at the Replit URL

## 🖥️ Option 2: Local (10 minutes)

```bash
# 1. Clone and setup
git clone <this-repo>
cd agentic-focus-group-workflow
./scripts/setup.sh

# 2. Add your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" >> .env

# 3. Run
python main.py

# 4. Open browser
open http://localhost:5000
```

## 🚀 First Workflow

Once running, try this example:

1. **Personas**: "Young professionals in Mumbai interested in sustainable products"
2. **Topic**: "Barriers to adopting eco-friendly lifestyle products"
3. **Click through each step** → Get realistic AI discussion!

## 🆘 Troubleshooting

- **"Invalid API key"**: Check your OpenAI API key in environment variables
- **"Module not found"**: Run `pip install -r requirements.txt`
- **"Permission denied"**: Run `chmod +x scripts/setup.sh`

## 📞 Need Help?

- Check `DEPLOYMENT.md` for detailed instructions
- Run `python monitoring/health_check.py` for diagnostics
- See `README.md` for complete documentation

**🎉 You're ready to create dynamic AI focus groups!**