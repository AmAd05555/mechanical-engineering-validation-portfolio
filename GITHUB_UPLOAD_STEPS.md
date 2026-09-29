# GitHub Upload Steps

## Recommended repository settings

**Repository name**
`mechanical-engineering-validation-portfolio`

**Description**
`Mechanical engineering portfolio: parametric CAD, FEA ground-truth validation, thermal analysis, Python engineering evaluation, and mechanical design.`

**Visibility**
Public

**Suggested topics**
`mechanical-engineering` `cad` `solidworks` `cadquery` `fea` `ansys` `python` `simulation` `thermal-analysis` `engineering-validation`

## Option A — GitHub Desktop (easiest for a folder with many files)
1. Create a new empty public repository on GitHub with the name above.
2. Do **not** add a README, .gitignore, or license during repository creation; this package already includes them.
3. Extract the ZIP package on your computer.
4. Open GitHub Desktop.
5. Choose **File → Add local repository** and select the extracted `amr-awad-engineering-portfolio` folder.
6. If GitHub Desktop asks to create a repository there, allow it.
7. Commit all files with the message: `Initial engineering portfolio`.
8. Publish/push the repository to the empty GitHub repository.

## Option B — Command line
After creating an empty GitHub repository, open a terminal inside the extracted folder and run:

```bash
git init
git add .
git commit -m "Initial engineering portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/mechanical-engineering-validation-portfolio.git
git push -u origin main
```

Replace `YOUR-USERNAME` with Amr's GitHub username.

## After publishing
1. Open the repository and verify that the root README renders correctly.
2. Open all five project links from the README.
3. Add the suggested topics in the repository settings/header.
4. Pin this repository on Amr's GitHub profile.
5. Copy the public repository URL.
6. Add that URL to the CV header as `Engineering Portfolio:` and to LinkedIn Featured.

## Recommended profile bio
`Mechanical Engineering Graduate | Parametric CAD | FEA & Thermal Validation | Python Engineering Automation`
