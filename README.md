<!-- <img width="3070" height="1106" alt="image" src="https://github.com/user-attachments/assets/88e1779b-b597-401d-9659-b744f8fbdb7d" /> -->
<img src="./readme/title1.svg"/>

<br><br>

<!-- project overview -->
<img src="./readme/title2.svg"/>

> GitMap is your companion for making sense of unfamiliar codebases. Instead of digging through endless folders, you get a clear visual map that shows how files are connected, letting you see the bigger picture at a glance.

>You can even ask natural language questions about any file, and the built-in AI agent will give you clear, contextual answers. Whenever something changes in your repository, GitMap keeps you in the loop with simple notifications, so you’re never caught off guard. On top of that, it uses machine learning to predict which parts of the code might be unstable, helping you spot risks early and focus your attention where it matters most.

>Whether you’re onboarding to a new project or keeping track of your own, GitMap turns messy repos into something you can actually understand and trust.


<br><br>

<!-- System Design -->
<img src="./readme/title3.svg"/>

### ER Diagram

View the live ER diagram here: [Eraser Workspace](https://app.eraser.io/workspace/NIzKPZnY8ZkSBtb8iS99?origin=share)

<p align="center">
  <img src="./readme/system-design/er_diagram.png" width="800px"/>
</p>





### System Architecture
<p align="center">
  <img src="./readme/system-design/system-architecture.png" width="800px"/>
</p>

<br><br>

<!-- Project Highlights -->
<!-- Project Highlights -->
<img src="./readme/title4.svg"/>

### Why GitMap Stands Out

- **Interactive Code Map** : instantly see how files connect through imports and dependencies.  
- **Natural Language Q&A with AI Agent** : ask plain-English questions about any file and explore the repo with contextual answers and guidance.  
- **Change Notifications** : stay up to date with simple alerts whenever your repository changes.  
- **Code Stability Predictions** : machine learning highlights risky or unstable areas of the code.

<br><br>

<img src="./readme/demo/figure.png"/>


<br><br>

<!-- Demo -->
<img src="./readme/title5.svg"/>


### User Screens (Web)

| Login screen                            | Register screen                       |
| --------------------------------------- | ------------------------------------- |
| ![Landing](./readme/demo/login.png) | ![fsdaf](./readme/demo/register.png) |


| Dashboard screen                            | My Repos screen                       |
| --------------------------------------- | ------------------------------------- |
| ![Landing](./readme/demo/dashboard.png) | ![fsdaf](./readme/demo/my-repos.png) |


| Map screen                            | Notifications screen                       |
| --------------------------------------- | ------------------------------------- |
| ![Landing](./readme/demo/map.png) | ![fsdaf](./readme/demo/notif.png) |


| Map Generation                          |
| --------------------------------------- |
| ![Landing](./readme/demo/map-gen.gif) |


| AI Agent                       |
| --------------------------------------- |
| ![Landing](./readme/demo/ai-agent.gif) |

| Machine Learning                        |
| --------------------------------------- |
| ![Landing](./readme/demo/ml.gif) |


<br><br>

<!-- Development & Testing -->
<img src="./readme/title6.svg"/>


| Services                            | Validation                       | Testing                        |
| --------------------------------------- | ------------------------------------- | ------------------------------------- |
| ![Landing](./readme/demo/services.png) | ![fsdaf](./readme/demo/validations.png) | ![fsdaf](./readme/demo/test.png) |

### Running Tests  

All tests can be run inside Docker containers without installing extra tools locally: use `docker compose run --rm backend python manage.py test -v 2` for backend (Django) tests and `docker compose run --rm frontend npm test -- --watchAll=false` for frontend (React) tests. The `--rm` flag ensures containers are removed after execution, keeping the environment clean. These same tests also run automatically in CI (GitHub Actions) on every push and pull request to the `main` and `dev` branches.

<br><br>

| Frontend Tests                          | Backend Tests                      |
| --------------------------------------- | ------------------------------------- |
| ![Landing](./readme/demo/frontend-tests.png) | ![fsdaf](./readme/demo/image.png) |

<br><br>
### AI Agent

**Simple Inputs:** The user just provides a GitHub repository URL.

**Smart Processing:** The system fetches code and commits, then the AI agent indexes and analyzes the repository.

**Clear Outputs:** The AI agent delivers easy-to-understand answers and insights based on the code.

<br><br>


| AI Agent Explanation                       |
| --------------------------------------- |
| ![Landing](./readme/demo/agent-exp.png) |

<br><br>


### Machine Learning

Our Random Forest model was trained on defect prediction data and evaluated on a held-out test set. The key metrics are:

**Accuracy:** 0.82 → The model correctly classifies ~82% of files overall.

**Precision:** 0.56 → When the model predicts a defect, it is correct about 56% of the time.

**Recall:** 0.23 → The model detects ~23% of actual defective files, meaning some are missed.

**F1 Score:** 0.32 → Balances precision and recall, showing moderate performance on defect detection.

These results indicate that the model is strong at identifying non-defective files, but recall for defective files is lower, a typical challenge in imbalanced datasets.

<br><br>


| Metrics Bar                          | 
| --------------------------------------- | 
| ![Landing](./readme/demo/metrics_bar.png) | 

<br><br>

| Confusion Matrix                          | ROC Curve                      |
| --------------------------------------- | ------------------------------------- |
| ![Landing](./readme/demo/confusion_matrix.png) | ![fsdaf](./readme/demo/roc_curve.png) |


<br><br>



### n8n Workflow

This workflow automatically checks watched GitHub repositories on a schedule, retrieves the latest **commit** information, and **compares** it with the stored commit reference. If new commits are found, it **updates** the record and sends a **notification** to the user, ensuring users are always informed about changes in their repositories.
<br><br>


| Workflow                         | 
| --------------------------------------- | 
| ![Landing](./readme/demo/n8n.png) | 

<br><br>

<!-- Deployment -->
<img src="./readme/title7.svg"/>

### API calls



| POST Add a GitHub repository            | GET code map data                     | POST Predict defects for repository files          |
| --------------------------------------- | ------------------------------------- | ------------------------------------- |
| ![Landing](./readme/demo/api_01.png) | ![fsdaf](./readme/demo/api_02.png) | ![fsdaf](./readme/demo/api_03.png) |

<br><br>

### Linear Board

I used **Linear** to stay organized and manage my workflow as a solo developer. Each task followed a clear cycle:

Create Ticket → Create Branch (Linear standard) → Make Commits (with task ID) → Push → Open Pull Request → Merge Pull Request

This kept my work structured and traceable from start to finish.

| Board                        |
| --------------------------------------- |
| ![Landing](./readme/demo/linear.png) |
