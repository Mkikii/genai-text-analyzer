# Best AI Prompts for GenAI Text Analyzer Project

## 🎯 Purpose of This Document

This document contains optimized AI prompts that were tested and refined to build the GenAI Text Analyzer. Each prompt is categorized by development phase and includes:
- The exact prompt to use
- Expected output type
- Why it works
- Tips for getting better results

---

## 📚 Phase 1: Understanding the Technology

### Prompt 1.1: FastAPI Introduction (Beginner)

```
I'm a Python developer familiar with Flask. Explain FastAPI in simple terms:
1. What makes it different from Flask?
2. When should I use FastAPI instead of Flask?
3. Show me a "Hello World" example with type hints
4. What are the 3 most important features for building APIs?

Keep it under 500 words with code examples.
```

**Why It Works:**
- Anchors to existing knowledge (Flask)
- Asks for specific comparisons
- Requests concrete examples
- Sets word limit for concise answers

---

### Prompt 1.2: OpenAI API Overview (Beginner)

```
I want to use OpenAI's GPT models in my Python application.
Explain like I'm a beginner:

1. What is the OpenAI API and what can it do?
2. How much does it cost? (ballpark estimate)
3. What's the difference between GPT-3.5-turbo and GPT-4?
4. Show me the simplest possible Python code to send text and get a response
5. What are "tokens" and why do they matter?

Include actual code I can copy-paste.
```

**Why It Works:**
- "Explain like I'm a beginner" sets the right level
- Asks about costs upfront (important!)
- Requests working code
- Addresses common confusion (tokens)

---

### Prompt 1.3: Pydantic Models (Intermediate)

```
In FastAPI, what are Pydantic models and why are they important?

Show me:
1. A basic Pydantic model for text input (with "text" field)
2. How to add validation (max length 5000 characters)
3. How to make fields optional
4. How FastAPI uses these models automatically

Use simple, real-world examples. Code first, explanation second.
```

**Why It Works:**
- Starts with practical code
- Progressive complexity
- Asks about the "why" and "how"

---

## 🏗️ Phase 2: Building the Core API

### Prompt 2.1: Creating First Endpoint (Beginner)

```
Create a complete FastAPI application that:
- Has one POST endpoint called /analyze
- Accepts JSON with a "text" field
- Returns JSON with: {"message": "Received: [the text]"}
- Includes proper imports and main app initialization
- Add comments explaining each part

Make it runnable with: uvicorn filename:app --reload
```

**Why It Works:**
- Very specific requirements
- Asks for completeness (imports, etc.)
- Requests comments for learning
- Includes run command

---

### Prompt 2.2: OpenAI Integration (Intermediate)

```
Integrate OpenAI GPT-3.5-turbo into this FastAPI endpoint.

Requirements:
- Keep the POST /analyze endpoint
- Use the openai library (not requests)
- Send the user's text to GPT-3.5-turbo
- Ask GPT to analyze sentiment and return JSON
- Handle the OPENAI_API_KEY from environment variable
- Add try-except for OpenAI errors

Show complete code with error handling. Explain the openai.ChatCompletion.create() parameters.
```

**Why It Works:**
- Builds on previous prompt
- Explicit about error handling
- Asks for parameter explanations
- Specifies library to use

---

### Prompt 2.3: Prompt Engineering for Structured Output (Advanced)

```
I'm calling GPT-3.5-turbo from my API. I need it to consistently return JSON with:
{
  "sentiment": "positive/negative/neutral",
  "key_phrases": ["phrase1", "phrase2", "phrase3"],
  "summary": "one sentence summary",
  "confidence": 0.95
}

Problems I'm facing:
1. Sometimes it returns text instead of JSON
2. Field names are inconsistent
3. key_phrases sometimes has too many/too few items

Create the optimal system and user prompt to fix this. Explain why your prompt structure works.
```

**Why It Works:**
- Shows exact desired output
- Lists specific problems
- Asks for explanation of solution
- Real-world scenario

---

### Prompt 2.4: Async Implementation (Advanced)

```
My FastAPI app is slow because OpenAI API calls are synchronous.

Current code:
[paste your sync code here]

Convert this to async/await pattern:
1. Make the endpoint async
2. Use async OpenAI calls
3. Explain when to use async vs sync
4. Show how to test it with curl

What performance improvement can I expect?
```

**Why It Works:**
- Provides context (performance issue)
- Shows current code
- Asks for specific improvements
- Includes testing method

---

## 🐳 Phase 3: Dockerization

### Prompt 3.1: Basic Dockerfile (Intermediate)

```
Create a production-ready Dockerfile for my FastAPI application.

Requirements:
- Python 3.11 slim base image
- Install from requirements.txt
- Expose port 8000
- Run with uvicorn
- Optimize for layer caching
- Not run as root user

Include comments explaining each line and why it's needed.
```

**Why It Works:**
- Specifies production-ready (not just working)
- Lists specific requirements
- Asks for optimization
- Requests educational comments

---

### Prompt 3.2: Docker Compose (Intermediate)

```
Create a docker-compose.yml for my FastAPI text analyzer:

- Service name: api
- Build from current directory
- Port mapping: 8000:8000
- Load OPENAI_API_KEY from .env file
- Auto-restart on failure
- Add health check endpoint

Also create a .env.example file showing what variables are needed.
```

**Why It Works:**
- Complete specification
- Includes related files (.env.example)
- Production considerations (restart, health)

---

## 🔧 Phase 4: Error Handling & Debugging

### Prompt 4.1: Error Handling (Advanced)

```
My FastAPI + OpenAI API has these error scenarios:
1. User sends empty text
2. Text is too long (> 4000 characters)
3. OpenAI API is down
4. OpenAI rate limit exceeded
5. Invalid API key

For each scenario:
- What HTTP status code should I return?
- What should the error message say?
- Show the FastAPI HTTPException code

Make error messages user-friendly but informative for debugging.
```

**Why It Works:**
- Lists all edge cases
- Asks for best practices (status codes)
- Wants user-friendly + developer-friendly
- Requests specific FastAPI patterns

---

### Prompt 4.2: CORS Debugging (Specific Problem)

```
I'm getting this error in my browser console:
"Access to fetch at 'http://localhost:8000/analyze' from origin 'http://localhost:3000' has been blocked by CORS policy"

My FastAPI app works in Postman but not from my React frontend.

1. What is CORS and why is this happening?
2. Show me the exact FastAPI middleware code to fix it
3. Explain each CORS parameter
4. Are there security concerns I should know about?
```

**Why It Works:**
- Shows actual error message
- Provides context (works in Postman)
- Asks for explanation + solution
- Considers security

---

### Prompt 4.3: Performance Optimization (Advanced)

```
My text analyzer API is too slow:
- Average response time: 8 seconds
- Using GPT-3.5-turbo
- No caching
- Synchronous calls

Suggest 5 optimizations I can implement today, ranked by:
1. Impact on performance
2. Ease of implementation

For each, show code example and expected improvement.
```

**Why It Works:**
- Provides metrics (8 seconds)
- Sets constraints (implement today)
- Asks for prioritization
- Wants quantified improvements

---

## 📊 Phase 5: Testing & Documentation

### Prompt 5.1: API Testing (Intermediate)

```
Create a complete testing strategy for my text analyzer API:

1. Write pytest code to test:
   - Valid text input
   - Empty text (should fail)
   - Very long text
   - Special characters and emojis

2. Mock the OpenAI API call (don't waste credits)

3. Test the /health endpoint

Show complete test file with imports and fixtures.
```

**Why It Works:**
- Comprehensive test cases
- Addresses cost concern (mocking)
- Asks for complete, runnable code

---

### Prompt 5.2: README Documentation (Beginner)

```
Write a professional README.md for my GenAI Text Analyzer project.

Include these sections:
- Project description with badges
- Features list (3-5 bullet points)
- Installation steps (Docker and local)
- API usage examples (curl and Python)
- Environment variables needed
- Deployment instructions
- Contributing guidelines

Make it beginner-friendly but professional. Use proper Markdown formatting.
```

**Why It Works:**
- Specifies exact sections needed
- Balanced tone (beginner + professional)
- Mentions formatting

---

## 🚀 Phase 6: Deployment

### Prompt 6.1: Railway Deployment (Specific)

```
I want to deploy my Dockerized FastAPI app to Railway.

Requirements:
1. Free tier is fine
2. Need to set OPENAI_API_KEY securely
3. Want automatic deployments from GitHub

Provide step-by-step instructions:
- What to prepare in my repo
- Railway configuration steps
- How to set environment variables
- How to check if it's running
- Common deployment issues and fixes
```

**Why It Works:**
- Names specific platform
- Sets constraints (free tier)
- Asks for complete workflow
- Includes troubleshooting

---

### Prompt 6.2: Production Checklist (Advanced)

```
My text analyzer API is going to production. Create a checklist of:

Security:
- [ ] List all security considerations

Performance:
- [ ] List performance optimizations

Monitoring:
- [ ] What should I monitor?

Cost:
- [ ] How to avoid surprise OpenAI bills?

For each item, explain WHY it matters and rate criticality (Critical/Important/Nice-to-have).
```

**Why It Works:**
- Organized by category
- Uses checklist format
- Asks for prioritization
- Practical considerations (cost)

---

## 🎨 Advanced Prompts

### Prompt 7.1: Multi-Language Support (Advanced)

```
Extend my text analyzer to support multiple languages.

Current: Only English
Goal: Support English, Spanish, French, Swahili

Requirements:
1. Auto-detect language
2. Translate to English before analysis (or analyze in original language?)
3. Return results in original language
4. Handle language detection errors

What's the best approach? Show code modifications needed.
Cost implications?
```

**Why It Works:**
- Clear current state vs goal
- Asks for architectural decision
- Considers cost
- Handles edge cases

---

### Prompt 7.2: Caching Strategy (Advanced)

```
Implement caching for my OpenAI API calls to reduce costs.

Scenario:
- Same text analyzed multiple times should use cache
- Cache should expire after 24 hours
- Need to store: text hash → API response

Compare these approaches:
1. In-memory dict (Redis)
2. SQLite database
3. File-based cache

For the best option, show:
- Complete implementation
- Cache hit/miss logging
- Memory/disk usage estimation
```

**Why It Works:**
- Explains business need (cost)
- Asks for comparison
- Wants metrics and monitoring

---

## 💡 Pro Tips for Using These Prompts

### Making Prompts More Effective

1. **Be Specific About Your Level**
   - ❌ "Explain FastAPI"
   - ✅ "Explain FastAPI to a Python developer familiar with Flask"

2. **Show What You've Tried**
   - ❌ "My code doesn't work"
   - ✅ "I'm getting this error: [exact error]. Here's my code: [paste code]"

3. **Ask for Examples**
   - ❌ "How do I validate input?"
   - ✅ "Show me 3 examples of Pydantic validation with comments"

4. **Set Constraints**
   - ❌ "Make it better"
   - ✅ "Optimize for speed, keeping code under 50 lines"

5. **Request Explanations**
   - ❌ "Give me the code"
   - ✅ "Show the code and explain why each part is needed"

---

## 🔄 Iterating on Prompts

### If the Response Isn't Helpful

**Follow-up Prompt Template:**
```
That's helpful, but I need more details on [specific part].

Specifically:
1. [What's unclear]
2. [What's missing]
3. [What needs examples]

Also, can you [specific request]?
```

### If You Get Too Much Information

**Refinement Prompt:**
```
That's too complex for my current level. 

Simplify it:
1. Remove advanced features
2. Focus only on [specific goal]
3. Limit to 200 words
4. Use a simple real-world example
```

---

## 📋 Quick Reference: Best Prompt Patterns

| Pattern | Example | Use When |
|---------|---------|----------|
| **Comparison** | "Compare FastAPI vs Flask for [use case]" | Learning new tech |
| **Step-by-step** | "Walk me through creating [feature] step by step" | Building something |
| **Debugging** | "I'm getting [error]. My code is: [code]. What's wrong?" | Fixing issues |
| **Optimization** | "My [metric] is [value]. Optimize for [goal]" | Improving performance |
| **Best practices** | "What are the top 5 mistakes to avoid when [doing X]?" | Quality assurance |

---

## 🎯 Project-Specific Prompt Template

For this GenAI Text Analyzer project, use this template:

```
I'm building a FastAPI text analyzer with OpenAI integration.

Current state: [what you have working]
Goal: [what you want to add/fix]
Constraints: [time, cost, complexity]

[Your specific question]

Requirements:
1. [Requirement 1]
2. [Requirement 2]

Show: [code/explanation/both]
```

---

**Remember:** The best prompt is specific, provides context, and asks for exactly what you need. Don't be afraid to iterate and refine!

---

**Last Updated**: November 27, 2024  
**Project**: GenAI Text Analyzer  
**Total Prompts**: 22 battle-tested prompts