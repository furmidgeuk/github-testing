How to Fork a Repository and Raise a PR in GitHub Without Write Access
If you don’t have write access to a repository but still need to submit a Pull Request (PR), you can do this by forking the repository and raising a PR from your fork.

🔹 Steps to Fork the Repository

Go to the Repository
Navigate to the GitHub repository you want to contribute to.
Fork the Repository
Click on the Fork button (top-right corner).
GitHub will create a copy of the repository under your account.
Clone Your Fork Locally
Open a terminal and run the following command:
git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
Replace YOUR-USERNAME with your GitHub username.
Replace REPO-NAME with the repository name.
Navigate to the Cloned Repo
cd REPO-NAME
🔹 Set Up the Upstream Repository

By default, your fork only knows about your own repository copy. You need to link it to the original repository to pull the latest changes.

Check the Current Git Remotes
git remote -v
You should see something like:

origin  https://github.com/YOUR-USERNAME/REPO-NAME.git (fetch)
origin  https://github.com/YOUR-USERNAME/REPO-NAME.git (push)
Add the Upstream Repository (Original Repo)
git remote add upstream https://github.com/ORIGINAL-OWNER/REPO-NAME.git
Replace ORIGINAL-OWNER with the actual owner of the repository.
Verify the Remote Repositories
git remote -v
You should now see:

origin    https://github.com/YOUR-USERNAME/REPO-NAME.git (fetch)
origin    https://github.com/YOUR-USERNAME/REPO-NAME.git (push)
upstream  https://github.com/ORIGINAL-OWNER/REPO-NAME.git (fetch)
upstream  https://github.com/ORIGINAL-OWNER/REPO-NAME.git (push)
🔹 Create a New Branch for Your Changes

Fetch the Latest Changes from Upstream
git fetch upstream
Create a New Branch
git checkout -b feat/my-new-feature upstream/main
Replace feat/my-new-feature with a meaningful branch name.
Make Your Changes
Modify the necessary files.
Save your changes.
Commit Your Changes
git add .
git commit -m "Add my new feature"
Push the Changes to Your Fork
git push origin feat/my-new-feature
🔹 Raise a Pull Request

Go to Your Fork on GitHub
Navigate to your forked repository (https://github.com/YOUR-USERNAME/REPO-NAME).
You should see a message prompting you to create a PR.
Click "Compare & pull request"
Ensure that:
Base repository = ORIGINAL-OWNER/REPO-NAME
Base branch = main (or the correct target branch)
Head repository = YOUR-USERNAME/REPO-NAME
Compare branch = feat/my-new-feature
Fill in the PR Details
Title: A short summary of your changes.
Description: Provide details about the changes, why they are needed, and any testing performed.
Submit the PR
Click "Create Pull Request".
🔹 Keep Your Fork Up to Date

If changes are made to the original repository while your PR is open, you may need to sync your fork.

Fetch Latest Changes from Upstream
git fetch upstream
Merge the Latest Changes
git checkout main
git merge upstream/main
Push to Your Fork
git push origin main
✅ Summary

Step	Command/Action
Fork the repo	Click Fork in GitHub
Clone your fork	git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
Set upstream remote	git remote add upstream https://github.com/ORIGINAL-OWNER/REPO-NAME.git
Create a feature branch	git checkout -b feat/my-new-feature upstream/main
Make and commit changes	git add . && git commit -m "My changes"
Push to your fork	git push origin feat/my-new-feature
Open a PR	GitHub → Compare & pull request
