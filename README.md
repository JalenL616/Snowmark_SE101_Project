# Snowmark (Portfolio Fork)
A smart grade prediction tool that transforms academic tracking into a targeted study plan.

**Note**: This repository is a fork of a university group project developed by a team of five over four weekly sprints. This fork serves as a portfolio piece highlighting my specific contributions to the codebase, architecture, and project management.

## My Contributions

As a core contributor and team lead, I focused on the application's primary logic, frontend interactivity, and project management.

**Technical Implementation**

 - **The Prediction Engine**: I engineered the core Python logic for the grade prediction algorithm, moving beyond simple linear regression to an exponential saturation model (detailed below).
 - **Dynamic Frontend (CRUD)**: Built the main assignments table using Vanilla JavaScript to handle inline editing, addition, and removal of grades without page reloads (using fetch API for asynchronous SQL updates).
 - **Category Weighting System**: Designed the logic for weighted grading schemes (e.g., Exams 40%, Homework 60%) with auto-validation to ensure totals equal 100%.
 - **Subject Management**: implemented the tab system for filtering assignments by course and the "Retire Subject" functionality.
 - **Landing Page**: Designed and implemented the public-facing landing page and demo assets.

## Project Management & Leadership

**Scrum Management**: Managed the issue board, led sprint planning, and organized the team into A/B sub-groups to tackle parallel tasks.

**Git Workflow**: Oversaw the majority of merge reviews and resolved conflicts between sprint branches.

## About Snowmark

Snowmark helps students work smarter by taking the guesswork out of academic planning. Instead of just tracking grades, it analyzes historical performance to provide personalized insights.

**Key Features**

 - **Grade Prediction**: Input a desired grade to see exactly how many hours you need to study, or input available time to predict your likely score.
 - **Performance Analytics**: Visualizes study efficiency (grades-per-hour) to identify which subjects are your strongest.
 - **Multi-Subject Dashboard**: Manage multiple courses with unique grading schemas and "Frosty" (Blue) or "Toasty" (Orange) color themes.
 - **Weighted Categories**: Full support for complex syllabi (e.g., Assignments, Labs, Midterms, Finals) with custom weights.

## The Algorithm

Unlike standard trackers that use simple averages, Snowmark uses an Exponential Learning Curve Model. We assumed that studying follows a law of diminishing returns—studying 2x longer does not guarantee a 2x higher grade.

**The Efficiency Parameter**: We use a learned variable specific to the user and subject. It is calculated using a trimmed mean of the user's historical performance, removing the bottom 20% of outliers to account for "bad study days."

**Cold Start**: For new users with no data, the system utilizes a weighted blend of global averages until sufficient personal data is logged.

## Tech Stack
**Backend**: Python, Flask, SQLAlchemy

**Database**: MySQL (Relational schema: Users ↔ Subjects ↔ Assignments)

**Frontend**: JavaScript (ES6), HTML5, CSS3, Jinja2 Templates

**Visualization**: Chart.js for statistical rendering

## Retrospective
This project was an exercise in Agile development under tight deadlines (4 weeks).

**Successes**: We successfully deployed a fully featured MVP including user authentication and persistent SQL storage. I personally grew significantly in Git management and Scrum leadership.

**Challenges**: Initial reliance on AI generation led to code organization issues, which required a significant refactor in Sprint 3 to modularize the logic.

**Future Improvements**: If I were to continue this project, I would implement stricter comprehensive testing suites (unit tests) to catch regression bugs earlier in the sprint cycle.
