# How to Run Your Reflection Tree

## ✅ You Have 3 Ways to Use It:

### 1. **Interactive Web Demo** (BEST for showing off!)
```bash
# Install dependencies
pip install Flask Flask-CORS

# Run server
python web_api.py

# Open browser
http://localhost:5001/demo
```

**What happens:**
- Beautiful web interface
- Click through questions
- See reflections in real-time
- Get personalized summary
- Progress bar shows where you are

**Perfect for:** Showing to recruiters, demos, presentations

---

### 2. **CLI Interactive Mode** (Original)
```bash
python agent/agent.py
```

**What happens:**
- Terminal-based conversation
- Type answers
- See colored output
- Get summary at end

**Perfect for:** Quick testing, command-line lovers

---

### 3. **Automated Personas** (For testing)
```bash
# Run victim persona (external locus, entitlement, self-centric)
python agent/agent.py --auto-path victim

# Run victor persona (internal locus, contribution, transcendent)
python agent/agent.py --auto-path victor
```

**What happens:**
- Runs automatically with pre-set answers
- Shows full conversation
- Proves the tree works
- Generates transcripts

**Perfect for:** Testing, validation, showing different paths

---

## 🎯 For Your DT Fellowship Submission

### Show Them the Web Demo!

1. **Start server:**
   ```bash
   python web_api.py
   ```

2. **Open:** `http://localhost:5001/demo`

3. **Walk through it** - answer questions honestly

4. **Take screenshots** of:
   - The questions
   - The reflections
   - The final summary

5. **Add to your voice note:**
   "I also built an interactive web version where users can walk through the tree in their browser. This makes it much more accessible than just a CLI tool."

---

## 📸 What It Looks Like

### Home Page (`http://localhost:5001/`)
- Professional landing page
- Explains the 3 axes
- Links to interactive demo
- API documentation

### Interactive Demo (`http://localhost:5001/demo`)
- Progress bar at top
- Questions with clickable options
- Reflections with icons
- Final summary with axis breakdown
- Beautiful gradient design

---

## 🚀 Deploy It (Optional but Impressive)

### Heroku
```bash
heroku create reflection-tree-diksha
git push heroku main
heroku open
```

Then you can say in your submission:
"Live demo: https://reflection-tree-diksha.herokuapp.com/demo"

---

## ✅ What to Submit

1. **GitHub:** https://github.com/Diksha159457/Role-Simulation
2. **Voice Note:** Mention you built both CLI and web versions
3. **Optional:** Deploy to Heroku and share live link

**The web demo makes your submission 10x more impressive!** 🎉