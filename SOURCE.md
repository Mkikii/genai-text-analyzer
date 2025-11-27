# Sources & References

**Project**: GenAI Text Analyzer  
**Author**: Maureen Karimi  
**Date**: November 2025

---

## 📚 Primary Learning Resources

### FastAPI Documentation & Tutorials

1. **FastAPI Official Documentation**
   - **Source**: https://fastapi.tiangolo.com/
   - **Used For**: Core framework concepts, endpoint creation, Pydantic models
   - **Key Sections**: 
     - Tutorial - User Guide
     - Advanced User Guide (async operations)
     - Deployment guide

2. **Real Python - FastAPI Tutorial**
   - **Source**: https://realpython.com/fastapi-python-web-apis/
   - **Used For**: Understanding FastAPI vs Flask differences
   - **Date Accessed**: November 2024

3. **freeCodeCamp - FastAPI Full Course**
   - **Source**: https://www.youtube.com/watch?v=7t2alSnE2-I
   - **Used For**: Comprehensive walkthrough of FastAPI features
   - **Duration**: 19 hours
   - **Topics Covered**: 
     - API development basics
     - Database integration
     - Authentication
     - Testing

4. **TestDriven.io - Building APIs with FastAPI**
   - **Source**: https://testdriven.io/blog/fastapi-crud/
   - **Used For**: CRUD operations and project structure
   - **Date Accessed**: November 2024

---

## 🤖 OpenAI Integration Resources

### OpenAI API Documentation

1. **OpenAI API Reference**
   - **Source**: https://platform.openai.com/docs/api-reference
   - **Used For**: 
     - Chat completions endpoint
     - API authentication
     - Error handling
     - Rate limits and pricing

2. **OpenAI Cookbook**
   - **Source**: https://github.com/openai/openai-cookbook
   - **Used For**: 
     - Best practices for prompt engineering
     - Examples of sentiment analysis
     - Token management strategies

3. **OpenAI Python Library**
   - **Source**: https://github.com/openai/openai-python
   - **Used For**: Python client implementation details
   - **Version Used**: 1.3.0+

---

## 🎓 Sentiment Analysis with AI Resources

1. **"Creating a Sentiment Prediction API with FastAPI" by Thierno Oumar Diallo**
   - **Source**: https://medium.com/@tod01/creating-a-sentiment-prediction-api-with-fastapi-4cd55e1c5340
   - **Used For**: Understanding FastAPI + ML integration patterns
   - **Key Takeaways**: 
     - Model serving architecture
     - Input/output validation patterns
     - Error handling strategies

2. **KDnuggets - "How to Create and Deploy a Simple Sentiment Analysis App via API"**
   - **Source**: https://www.kdnuggets.com/2021/06/create-deploy-sentiment-analysis-app-api.html
   - **Used For**: HuggingFace Transformers integration (for comparison)
   - **Key Learnings**: Pipeline abstractions, deployment strategies

3. **"Mastering Sentiment Analysis through Generative AI" - Analytics Vidhya**
   - **Source**: https://www.analyticsvidhya.com/blog/2023/09/mastering-sentiment-analysis-through-generative-ai/
   - **Used For**: 
     - Prompt engineering for sentiment analysis
     - Handling multilingual reviews
     - GPT-3.5 temperature settings

4. **"Quick and Easy: Sentiment Analysis with LLM" by Wilasinee Paewboontra**
   - **Source**: https://medium.com/@beam_villa/quick-and-easy-sentiment-analysis-with-llm-c61c562d059c
   - **Used For**: 
     - Prompt templates for sentiment extraction
     - Comparison of Gemini vs GPT for sentiment tasks

---

## 🐳 Docker & Deployment Resources

### Docker Documentation

1. **Docker Official Documentation**
   - **Source**: https://docs.docker.com/
   - **Used For**: 
     - Dockerfile best practices
     - Multi-stage builds
     - Environment variable management
   - **Sections Used**:
     - Get started
     - Docker Compose
     - Best practices for writing Dockerfiles

2. **FastAPI in Containers - Docker**
   - **Source**: https://fastapi.tiangolo.com/deployment/docker/
   - **Used For**: FastAPI-specific Docker configurations
   - **Key Learnings**: 
     - Optimal base images for FastAPI
     - Uvicorn configuration in Docker
     - Health check implementations

### Deployment Platforms

1. **Railway Deployment Documentation**
   - **Source**: https://docs.railway.app/guides/fastapi
   - **Used For**: Railway-specific deployment steps
   - **Topics**: Environment variables, automatic deployments

2. **Render FastAPI Deployment Guide**
   - **Source**: https://render.com/docs/deploy-fastapi
   - **Used For**: Alternative deployment option
   - **Topics**: Web service configuration, environment setup

---

## 🛠️ Development Tools & Libraries

### Python Libraries Documentation

1. **Pydantic Documentation**
   - **Source**: https://docs.pydantic.dev/
   - **Version**: 2.0+
   - **Used For**: 
     - Data validation models
     - Type hints and validation
     - JSON schema generation

2. **Uvicorn Documentation**
   - **Source**: https://www.uvicorn.org/
   - **Used For**: 
     - ASGI server configuration
     - Async request handling
     - Production deployment settings

3. **Python-dotenv Documentation**
   - **Source**: https://pypi.org/project/python-dotenv/
   - **Used For**: Environment variable management

---

## 💡 AI-Assisted Learning

### Prompts Used with GenAI

All prompts documented in Section 6 of CAPSTONE_TOOLKIT.md were executed using:

1. **Claude (Anthropic)**
   - **Platform**: ai.moringaschool.com
   - **Model**: Claude Sonnet 4.5
   - **Used For**: 
     - FastAPI architecture questions
     - Code generation and debugging
     - Prompt engineering strategies
     - Docker configuration

2. **ChatGPT (OpenAI)**
   - **Platform**: chat.openai.com
   - **Model**: GPT-4
   - **Used For**: 
     - Alternative perspectives on implementation
     - Debugging complex errors
     - Best practices validation

---

## 📖 Academic & Research Papers

1. **"Attention Is All You Need" (Transformer Architecture)**
   - **Authors**: Vaswani et al.
   - **Year**: 2017
   - **Relevance**: Foundational paper for GPT models
   - **Source**: https://arxiv.org/abs/1706.03762

2. **"Language Models are Few-Shot Learners" (GPT-3)**
   - **Authors**: Brown et al., OpenAI
   - **Year**: 2020
   - **Relevance**: Understanding GPT-3 capabilities
   - **Source**: https://arxiv.org/abs/2005.14165

---

## 🌐 Community Resources

### Forums & Discussion

1. **Stack Overflow - FastAPI Tag**
   - **Source**: https://stackoverflow.com/questions/tagged/fastapi
   - **Used For**: Troubleshooting specific errors
   - **Key Questions Referenced**:
     - CORS middleware configuration
     - Async/await best practices
     - Pydantic model validation

2. **Reddit - r/FastAPI**
   - **Source**: https://www.reddit.com/r/FastAPI/
   - **Used For**: Community best practices and patterns

3. **FastAPI Discord Community**
   - **Source**: https://discord.gg/VQjSZaeJmf
   - **Used For**: Real-time help and discussions

---

## 📊 Similar Projects Studied

### GitHub Repositories (for inspiration and learning)

1. **curiousily/Deploy-BERT-for-Sentiment-Analysis-with-FastAPI**
   - **Source**: https://github.com/curiousily/Deploy-BERT-for-Sentiment-Analysis-with-FastAPI
   - **Used For**: Understanding BERT integration patterns
   - **Key Takeaways**: Model serving architecture, response formatting

2. **mahinuralam/Fast-API-Sentiment-Analysis**
   - **Source**: https://github.com/mahinuralam/Fast-API-Sentiment-Analysis
   - **Used For**: RESTful API design patterns for sentiment analysis
   - **Key Takeaways**: CRUD operations, database integration

3. **shabisht/Sentiment-Analysis-API**
   - **Source**: https://github.com/shabisht/Sentiment-Analysis-API
   - **Used For**: Production deployment strategies
   - **Key Takeaways**: Model evaluation, preprocessing pipelines

4. **sadasystems/sentiment-analysis-genai**
   - **Source**: https://github.com/sadasystems/sentiment-analysis-genai
   - **Used For**: Google Cloud PaLM integration examples
   - **Key Takeaways**: Alternative GenAI providers

---

## 🎬 Video Tutorials

1. **"FastAPI Tutorial for Beginners" - Traversy Media**
   - **Source**: https://www.youtube.com/watch?v=0sOvCWFmrtA
   - **Duration**: 1 hour
   - **Used For**: Quick start guide and best practices

2. **"OpenAI API Crash Course" - Dave Gray**
   - **Source**: https://www.youtube.com/watch?v=c-g6epk3fFE
   - **Duration**: 40 minutes
   - **Used For**: OpenAI API integration fundamentals

3. **"Build a REST API with FastAPI, PostgreSQL and SQLAlchemy"**
   - **Source**: https://www.youtube.com/watch?v=2g1ZjA6zHRo
   - **Duration**: 3 hours
   - **Used For**: Database integration patterns (for future enhancements)

---

## 📝 Blog Posts & Articles

1. **"Build a Sentiment & Entity Detection API with FastAPI" - Shane Lynn**
   - **Source**: https://www.shanelynn.ie/build-a-sentiment-entity-detection-api-with-fastapi-2-2/
   - **Date**: December 2021
   - **Used For**: 
     - Spacy integration examples
     - API response formatting
     - Testing strategies

2. **"Exploring Sentiment Analysis with Generative AI" by Dharmaraj**
   - **Source**: https://medium.com/@draj0718/exploring-sentiment-analysis-with-generative-ai-95dd617a396f
   - **Date**: December 2023
   - **Used For**: 
     - Google Generative AI integration
     - Prompt templates for sentiment analysis

---

## 🔧 Tools & Platforms Used

### Development Environment

1. **Visual Studio Code**
   - **Source**: https://code.visualstudio.com/
   - **Extensions Used**:
     - Python (Microsoft)
     - Docker (Microsoft)
     - REST Client

2. **Postman**
   - **Source**: https://www.postman.com/
   - **Used For**: API testing and documentation

3. **Docker Desktop**
   - **Source**: https://www.docker.com/products/docker-desktop
   - **Used For**: Containerization and local development

### Cloud Services

1. **GitHub**
   - **Source**: https://github.com/
   - **Used For**: Version control and code hosting
   - **Repository**: https://github.com/Mkikii/genai-text-analyzer

2. **OpenAI Platform**
   - **Source**: https://platform.openai.com/
   - **Used For**: API key management and usage monitoring

---

## 📖 Books Referenced

1. **"Building Data Science Applications with FastAPI" by François Voron**
   - **Publisher**: Packt Publishing
   - **Year**: 2021
   - **ISBN**: 978-1801079211
   - **Chapters Used**: 1-4 (FastAPI fundamentals)

2. **"Prompt Engineering for ChatGPT: A Quick Guide to Techniques, Tips, and Best Practices"**
   - **Authors**: Mike Taylor et al.
   - **Publisher**: O'Reilly Media
   - **Year**: 2023
   - **Used For**: Prompt design strategies

---

## 🏆 Best Practices Sources

1. **Twelve-Factor App Methodology**
   - **Source**: https://12factor.net/
   - **Used For**: 
     - Environment variable management
     - Configuration best practices
     - Deployment strategies

2. **REST API Best Practices**
   - **Source**: https://restfulapi.net/
   - **Used For**: 
     - HTTP status codes
     - Endpoint naming conventions
     - Error handling patterns

3. **OpenAPI Specification**
   - **Source**: https://swagger.io/specification/
   - **Used For**: API documentation standards

---

## 🔐 Security Resources

1. **OWASP API Security Top 10**
   - **Source**: https://owasp.org/www-project-api-security/
   - **Used For**: Understanding common API vulnerabilities
   - **Focus Areas**:
     - Broken authentication
     - Excessive data exposure
     - Rate limiting

2. **FastAPI Security Documentation**
   - **Source**: https://fastapi.tiangolo.com/tutorial/security/
   - **Used For**: Authentication and authorization patterns

---

## 📊 Performance & Monitoring

1. **"Monitoring FastAPI Applications with Prometheus"**
   - **Source**: https://dev.to/ken_mwaura1/monitoring-fastapi-apps-with-prometheus-and-grafana-2g5a
   - **Used For**: Future monitoring implementation

2. **Uvicorn Performance Tuning**
   - **Source**: https://www.uvicorn.org/deployment/
   - **Used For**: Production deployment optimization

---

## 🎓 Moringa School Resources

1. **Moringa AI Platform**
   - **Source**: https://ai.moringaschool.com
   - **Used For**: AI-assisted learning and problem-solving
   - **Features Used**:
     - Code generation
     - Debugging assistance
     - Concept explanations

2. **Capstone Project Guidelines**
   - **Source**: Provided by instructor
   - **Used For**: Project structure and requirements

---

## 📅 Citation Format

All sources were accessed and verified between **November 20-27, 2024** unless otherwise specified.

**Citation Style**: MLA 9th Edition adapted for software development projects

---

## ✅ Source Verification

All code examples from external sources were:
- ✅ Tested in development environment
- ✅ Adapted to project requirements
- ✅ Documented in commit messages
- ✅ Attributed in code comments where significant

---

## 📝 Notes

- **AI-Generated Code**: All AI-generated code was reviewed, tested, and modified as needed
- **External Libraries**: All external libraries are properly cited in `requirements.txt`
- **License Compliance**: All referenced projects are open source (MIT, Apache 2.0)

---

**Last Updated**: November 27, 2025  
**Total Sources**: 50+  
**Primary Documentation**: FastAPI, OpenAI API, Docker  
**Key Learning Method**: AI-assisted learning with practical implementation