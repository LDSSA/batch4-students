# Batch 4 Students Repository

Welcome to Lisbon Data Science Academy Batch 4 Students repository!

Here is you'll find all information needed to setup your environment and the
workflow you'll use during the academy.

1. [Initial Setup](#initial-setup)
    1. [Windows Setup](#Windows-Setup)
    1. [MacOS Setup](#MacOS-Setup)
    1. [Ubuntu Setup](#Ubuntu-Setup)
    1. [Setup for all Operating Systems](#Setup-for-all-Operating-Systems)
    1. [Setup Git and GitHub](#Setup-Git-and-GitHub)
    1. [Setup your Workspace Repository](#setup-your-workspace-repository)
    1. [Get the Learning Material](#get-the-learning-material)
    1. [Running and Submitting a Learning Unit](#running-and-submitting-a-learning-unit)
1. [Learning Unit Workflow](#learning-unit-workflow)
1. [Updates to Learning Units](#updates-to-learning-units)
1. [Help](#help)
    1. [Learning Unit](#learning-unit-workflow)
    1. [_Portal_](#_portal_)
    1. [Troubleshooting](#Troubleshooting)
    1. [Other](#other)

## Initial Setup

**IMPORTANT**
Before the bootcamp you will have to complete these instructions, this is
essential.

Once you complete the setup mark yourself as such on [this spreadsheet](https://docs.google.com/spreadsheets/d/1bEOwvEmEJONYzW94efixHa8Te8I_QKC91m8WPoADxjY/edit?usp=sharing).

By completing this you will setup and learn about all the tools you'll be
using during the academy.
We will also be able to identify any problems in time to figure out a solution.

### Windows Setup

This section deals with setting up either Windows Subsystem for Linux (WSL)
or VMWare.
If you are using MacOS or Linux you can skip this section.

If you are using windows 10 we suggest using WSL (see below), if you are using an older Windows version we also support running a virtual linux machine with VMWare.

**Why do I need to install either WSL or VMware?**

Because of the differences in command line syntax between Windows vs Mac OS/Linux, it would be a great challenge for us to support and provide instructions for both Operating Systems. For this reason, we’d ask you to install Windows Subsystem for Linux, or VMware, which would enable you to run Linux command lines inside Windows. Keep in mind that these are simply extensions to your Windows operating system, hence, installing this software will not do any changes on your laptop. It is also quick to do so.

#### Windows 10 Setup

Follow [this guide](guides/Windows_Subsystem_for_Linux_Installation_Guide_for_Windows_10.md) if you are running Windows 10.

#### Older Windows Setup

If you are running an older version of Windows (such as Windows 8 or 7), follow the guide below on running Ubuntu with Windows using VMware Player. You'll be required to download VMware and Ubuntu 18, for that please use the links provided below (not the links provided in the tutorial).

* [VMware download link](https://www.vmware.com/go/getplayer-win)
* [Ubuntu download link](https://ubuntu.com/download/desktop/thank-you?version=18.04.4&architecture=amd64)
* Follow this guide: [How To Run Ubuntu in Windows 7 with VMware Player](https://www.howtogeek.com/howto/11287/how-to-run-ubuntu-in-windows-7-with-vmware-player/)

You'll now need to install a couple of packages,
which can be done in a terminal by running:

```bash
sudo apt update && sudo apt upgrade && sudo apt install python3-pip python3-venv
```

### MacOS Setup

Some of the steps in the following sections will require _Homebrew_ for MacOS.
Homebrew will make it easier to install software that we will use later on.
To open the terminal, choose one:

* In Finder <img src='assets/finder.png' alt='Finder' width="4%" height="4%"/>, open the /Applications/Utilities folder, then double-click Terminal.
* By pressing <kbd>cmd</kbd> + <kbd>space</kbd> then type `terminal` and press <kbd>enter</kbd>.

The terminal should now be open:

![mac_terminal](assets/mac_terminal.png)

Copy and paste the following line in the terminal:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

You may be offered to install the _Command Line Developer Tools_, confirm and
once it's finished continue installing Homebrew by pressing <kbd>enter</kbd> again.

You will need to install python, this can be done in a terminal by running:

```bash
brew install python
```

### Ubuntu Setup

So you're using Ubuntu, hun? Well, kudos to you.

You just need to install a couple of packages,
which can be done in a terminal by running:

```bash
sudo apt update && sudo apt upgrade && sudo apt install python3-pip python3-venv
```

### Setup for all Operating Systems

#### Creating a Python Virtual Environment

Bellow are the instructions that are enough to get the setup done and get you up and running :)
You can also follow [this guide](guides/How_to_set_up_python_virtual_environments.md) for a more in depth set of instructions that accomplish exactly the same thing.

You should always be using a virtual environment to install python packages. We'll use _venv_ to set them up.

To install and update packages, we'll be using _pip_ which is the reference Python package manager.

##### Start by installing ensuring pip, setuptools, and wheel are up to date:

```bash
python3 -m pip install --user --upgrade pip setuptools wheel
```

* Create a virtual environment with the name `slu00`

```bash
python3 -m venv ~/.virtualenvs/slu00
```

* Activate the environment

```bash
source ~/.virtualenvs/slu00/bin/activate
```

>Note: after you activate your virtual environment you should see at the leftmost of your command line the name of your virtual environment surrounded by parenthesis, like this:

```bash
mig@my-machine % source ~/.virtualenvs/slu00/bin/activate
(slu00) mig@my-machine %
```

And you're able to make sure your virtual environment is active using the `which` command (it outputs the location of your virtual environment's python installation):

```bash
(slu00) mig@my-machine % which python
/Users/mig/.virtualenvs/slu00/bin/python
```

Now update pip.

```bash
(slu00) pip install -U pip
```

### Setup Git and GitHub

Having a _GitHub_ account and knowing the basics of committing and pushing
changes are mandatory.
By the end of this setup you will have accomplished both.
Complete the following steps:

1. [Sign up](https://github.com/join) for a _GitHub_ account if you don't
already have one.
1. [Checking for existing SSH keys](https://help.github.com/en/github/authenticating-to-github/checking-for-existing-ssh-keys)
1. [Generating a new SSH key and adding it to the ssh-agent](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
1. [Adding a new SSH key to your GitHub account](https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account)
1. [Testing your SSH connection](https://help.github.com/en/github/authenticating-to-github/testing-your-ssh-connection)

### Setup your Workspace Repository

It's good practice to store your work with version control.
In this academy that is a requirement as it is how you will make your work
available to us.

#### Creating the Workspace

1. Log into _GitHub_
1. Create a new **private** _GitHub_ repository called *batch4-workspace*, see
[Creating a new repository](https://help.github.com/en/articles/creating-a-new-repository).
**IMPORTANT** The repo **MUST** be named *batch4-workspace*!
If you name it anything else, you will be unable to submit any of your work!
    1. You need to explicitly select Private - This is your work and nobody else's.
    You will be graded based upon the merits of what you are able to do here
    so this should not be open to the world while you are working
    on it.
    Maybe after the course is completed, you can open-source it but not this
    time.
    1. Initialize with a README.
    This is mostly just so that you don't initialize an empty repo.
    1. Add a Python `.gitignore`.
    This step is insanely important. If you don't do this, you may
    end up checking things into the repo that make it un-gradeable by our
    grading system.
    ADD THE `.gitignore` PLEASE!!!! <--- 4 * `!` isn't enough

![Create Repository](assets/create_repository.png "Create Repository")

#### Add a Deploy Key to your Repository

Since the repository is private you will have to explicitly give access so
that our grading system can fetch the repository.
To do this you will be adding a deploy key to the repository, which we
provide to you in our [_Portal_](https://portal.lisbondatascience.org/).

1. Head on to the [_Portal_](https://portal.lisbondatascience.org/)
1. Log in with your _GitHub_ account
1. Go to your [profile](https://portal.lisbondatascience.org/users/info/) and
copy the deploy key (including the `ssh-rsa` part)
![Profile](assets/profile.png "Profile")
1. Go back to the repository you have just created
1. Go to `Settings > Deploy Keys`
1. Click "Add deploy key" (no need to grant Write Access)
1. Give it a recognizable name like "grader" and paste the key from the
_Portal_
![Deploy keys](assets/deploy_key.png "Deploy key")

#### Cloning the Workspace

1. Open a Terminal or Git Bash, the next steps are on this terminal
1. Clone your `<username>/batch4-workspace` repository

    > If you're not sure where to clone the repository in, you can create a `~/projects` folder, and clone it there

```bash
git clone git@github.com:<username>/batch4-workspace.git
```

### Get the Learning Material

You will be cloning the [batch4-students](https://github.com/LDSSA/batch4-students)
repository.
All of the learning material you need will be made available on this repo
as the academy progresses.

1. Open a Terminal or Git Bash, the next steps are on this terminal
1. Clone the students repository
[batch4-students](https://github.com/LDSSA/batch4-students)

```bash
git clone https://github.com/LDSSA/batch4-students.git
```

Or if you have your ssh keys set up:

```bash
git clone git@github.com:LDSSA/batch4-students.git
```

### Running and Submitting a Learning Unit

In the `batch4-students` repository that you just cloned there is a sample
learning unit.
It's used to give instructors guidelines to produce the learning units.
We are also using it to ensure that you are able to run and submit a learning
unit.

So go ahead and copy the sample directory `sample/SLU00 - LU Tutorial` from the `batch4-students` repository to your repository (named `batch4-workspace`).
![Sample learning unit](assets/sample_learning_unit.png "Sample learning unit")

The grader only requires you to have the contents in a directory starting with
the learning unit's ID, but we highly advise to keep the same directory
structure as the students repository.
All learning units are organized as:

```markdown
<specialization ID> - <specialization name>/<learning unit ID> - <learnin unit name>
```

Doing so will help you keep organized and ease copying data from the students
repository to yours.

#### Working on the Learning Unit

All learning units come as a set of Jupyter Notebooks (and some links to
presentations).
Notebooks are documents that can contain text, images and live code that you
can run interactively.

In this section we will launch the Jupyter Notebook application.
The application is accessed through the web browser.

Once you have the application open feel free to explore the sample learning
unit structure.
It will give you a handle on what to expect and what rules the instructors
follow (and the effort they put) when creating a learning unit.

So let's start the Jupyter Notebook app:

1. Activate your virtual environment

    ```bash
    source ~/.virtualenvs/slu00/bin/activate
    ```

1. Enter the Learning unit directory in your workspace directory (`batch4-workspace`).
    >Note: It is **VERY IMPORTANT** that you **ALWAYS** work on the files on your `batch4-workspace` repository, and **NEVER** work on files that are in your `batch4-students` repository!

    ```bash
    cd ~/projects/batch4-workspace/"Week 0"/"SLU00 - Jupyter Notebook"
    ```

1. Installing the necessary packages

    ```bash
    pip install -r requirements.txt
    ```

1. Run the jupyter notebook
    >**Windows 10 note:** if you are running **Windows 10** with WSL, the command to run the jupyter notebook is: `jupyter notebook --NotebookApp.use_redirect_file=False`

    ```bash
    jupyter notebook
    ```

When you run the `jupyter notebook` command, you should see something similar to this in your terminal:
![Open exercise notebook](assets/jupyter_terminal.png "Open exercise notebook")
Your browser should pop up with Jupyter open, however, if this does not happen, you can simply copy the link you see on your terminal (the one that contains `localhost`) and past it in your browser's address bar:

![Open exercise notebook](assets/jupyter_terminal_link.png "Open exercise notebook")

>Note: If you see these scarry looking error messages, don't worry, you can just ignore them.

![Open exercise notebook](assets/jupyter_error_red.png "Open exercise notebook")

##### The Exercise Notebook

Make sure you open and go through the Learning Notebook first.

Every learning unit contains an exercise notebook with exercises you will
work on.
So let's have a look at the sample Learning Unit.

1. On the Jupyter Notebook UI in the browser open the exercise notebook
![Open exercise notebook](assets/jupyter_exercise_notebook.png "Open exercise notebook")
1. Follow the instructions provided in the notebook

Besides the exercises and the cells for you to write solutions you will see
other cells with a series of `assert` statements.
This is how we (and you) will determine if a solution is correct.
If all `assert` statements pass, meaning you dont get an `AssertionError` or
any other kind of exception, the solution is correct.

Once you've solved all of the notebook we recommend the following this simple
checklist to avoid unexpected surprises.

1. Save the notebook (again)
1. Run "Restart & Run All"
![Restart & Run All](assets/jupyter_clear_and_run.png "Restart & Run All")
1. At this point the notebook should have run without any failing assertions

If you want to submit your notebook before it is all the way done to
check intermediate progress, feel free to.

If you are able to go through the entire process and get a passing grade on
the sample LU you'll have a good understanding of the same flow that you'll use
for all LUs throughout the academy.

#### Commit and Push

Now you have worked on the sample learning unit and you have some uncommitted
changes.
It's time to commit the changes, which just means adding them to your `batch4-workspace`
repository history, and pushing this history to you remote on _GitHub_.

* Using the terminal commit and push the changes

```bash
git add .
git commit -m 'Testing the sample notebook'
git push
```

#### Grading

1. Go to the [_Portal_](https://portal.lisbondatascience.org) and select the learning unit
![Learning unit](assets/portal_sample_lu.png "Learning unit")
1. Select "Grade"
![Grade](assets/portal_grade.png "Grade")
1. After grading is complete you should have 20/20
1. If everything passes locally but the grader doesn't give you the excepted
output head to out [troubleshooting](#_portal_)
1. Once you have your grade don't forget to do the
[spreadsheet](https://docs.google.com/spreadsheets/d/1bEOwvEmEJONYzW94efixHa8Te8I_QKC91m8WPoADxjY/edit?usp=sharing) thing.

## Learning Unit Workflow

You will need to follow this workflow every week starting from week 1.

Learning units will be announced in the academy's _#announcements_ channel.
At this point they are available in the
[batch4-students](https://github.com/LDSSA/batch4-students)
repository.
A new Learning Unit is released every Monday, and its
solutions are then released the next Monday.

The steps you followed during the initial setup are exactly what you are going
to be doing for each new Learning Unit.
Here's a quick recap:

1. Once a new Learning Unit is available at the beginning of each week, pull the changes from the [batch4-students](https://github.com/LDSSA/batch4-students) repo:
    * enter the `~/projects/batch4-students/` using the `cd` command, then use the `git pull` command:

    ```bash
    cd ~/projects/batch4-students/
    git pull
    ```

    >note that this will also pull the solutions for the Learning Unit of the previous week

1. Copy the Learning Unit to your `batch4-workspace` repo

    * To do that you can use the `cp` command:

    ```bash
    cp -r ~/projects/batch4-students/"Week <week number>" ~/projects/batch4-workspace
    ```

    and you would replace the `<week number>` with the week number, such that in week 0, for example, the command would be:

    ```bash
    cp -r ~/projects/batch4-students/"Week 0" ~/projects/batch4-workspace
    ```

1. Create a new virtual environment for the Learning Unit you'll be working on.

    * To do this you will run the following command:

    ```bash
    python3 -m venv ~/.virtualenvs/<Learning Unit name>
    ```

    * and you would replace the `<Learning Unit name>` with the Learning Unit name, such that for SLU00, for example, the command would be:

    ```bash
    python3 -m venv ~/.virtualenvs/slu00
    ```

1. Activate your virtual environment

    ```bash
    source ~/.virtualenvs/slu00/bin/activate
    ```

1. Install the python packages from requirements.txt for the specific SLU (you must do this for each SLU, and there are multiple SLU's in a Week)

    ```bash
    pip install -r ~/projects/batch4-workspace/"Week <week number>"/"<SLU name>"/requirements.txt
    ```

    and you would replace `<week number>` and `<SLU name>`, such that in Week 0 and SLU000 - Jupyter Notebook, for example, the command would be:

    ```bash
    pip install -r ~/projects/batch4-workspace/"Week 0"/"SLU000 - Jupyter Notebook"/requirements.txt
    ```

1. Change to the `batch4-workspace` dir

    ```bash
    cd ~/projects/batch4-workspace
    ```

1. Open Jupyter Notebook

    ```bash
    jupyter notebook
    ```

1. Work
1. Once all tests pass or once you're happy, save your work, close the browser tab with the Jupyter Notebook, close the terminal and open a new terminal
1. Then commit the changes and push

    ```bash
    cd ~/projects/batch4-workspace
    git add .
    git commit -m "Work on week <week number> exercises"
    git push
    ```

1. Profit

## Updates to Learning Units

As much as we try and have processes in place to prevent errors and bugs in
the learning units some make it through to you.
If the problem is not in the exercise notebook you can just pull the new
version from the students repo and replace the file.
The problem is if the correction is in the exercise notebook, you can't just
replace the file your work is there and you'll lose it!

When a new version of the exercise notebook is released (and announced) two
things will happen.
If you submit an old version of the notebook it will be flagged as out of date
and not graded.
You will have to merge the work you've already done into the new version of the
notebook.

At the moment our suggestion to merge the changes is:

1. Rename the old version
1. Copy the new exercise notebook over
1. Open both and copy paste your solutions to the new notebook

We understand it's not ideal and are working on improving this workflow using
[_nbdime_](https://nbdime.readthedocs.io/).
If you are comfortable installing _Python_ packages you can try it out, but
we offer no support for this at the moment.

## Help

During the academy you will surely run into problems and have doubts about the
material.
We provide you with some different channels to ask for help.

### Learning Unit

If you feel something is not clear enough or there is a bug in the learning
material please follow [these steps](https://github.com/LDSSA/wiki/wiki/How-to-ask-for-and-give-help). Remember, there is no such thing as a dumb question, and by asking questions publicly you will help others!

If you have more conceptual questions about the materials or how to approach a problem you can also
reach out to the instructors on slack.
You can find the main contact for the learning unit in the
[_Portal_](https://portal.lisbondatascience.org/) this instructor can help you
out or redirect you to someone that is available at the moment.

### _Portal_

Are you getting different results locally than what you are getting in the
_Portal_?
If so we will first ask to do a bit of troubleshooting.

1. Ensure that you have saved the changes in the notebook
1. Ensure that you have committed and pushed the changes
1. Ensure that you are not using packages that are not present in the original
`requirements.txt` file (changes to this file or your local environment have no
effect)
1. In the learning unit page in the [_Portal_](https://portal.lisbondatascience.org/)
you are able to download the exercise notebook with the results of the grader
by clicking your grade, have a look to figure out what went wrong.
![Download notebook](assets/portal_download_notebook.png "Download notebook")
If none of these steps helped go ahead and open a support ticket for the portal
[here](https://github.com/LDSSA/batch4-portal-support).

Is the _Portal_ down or acting out in some unexpected way?
Then please open a support ticket for the portal
[here](https://github.com/LDSSA/batch4-portal-support).

### Troubleshooting

1. [When I open Windows Explorer through Ubuntu it goes to a different folder than in the guide](#When-I-open-Windows-Explorer-through-Ubuntu-it-goes-to-a-different-folder-than-in-the-guide)
1. [Ubuntu on Windows 10 high CPU usage crashes](#Ubuntu-on-Windows-10-high-CPU-usage-crashes)
1. [When I pull from the `batch4-students` repository I get an error](#When-I-pull-from-the-batch4-students-repository-I-get-the-error)
1. [When I try to open `jupyter notebook` I get an error](#When-I-try-to-open-jupyter-notebook-I-get-the-error)
1. [When I use the `cp` command the `>` sign appears and the command does not execute](#When-I-use-the-`cp`-command-the->-sign-appears-and-the-command-does-not-execute)
1. [My problem is not listed here what should I do?](#My-problem-is-not-listed-here-what-should-I-do?)

#### When I open Windows Explorer through Ubuntu it goes to a different folder than in the guide

Please make sure:

* you are running the command `explorer.exe .` including the dot at the end.
* you are running Windows 10 version `1909` or newer.

#### Ubuntu on Windows 10 high CPU usage crashes

* First please make sure you are running Windows 10 version `1909` or newer.
* Then, try following [these steps](https://teckangaroo.com/enable-windows-10-virtual-machine-platform/)

#### When I pull from the `batch4-students` repository I get the error

```bash
error: Your local changes to the following files would be overwritten by merge:
<some files>
Please commit your changes or stash them before you merge.
Aborting
```

_git_ is telling us that changes were made by you to the files on the `~/projects/batch4-students` folder, and is not pulling the changes made by the instructors because they would override the changes that you made there. To fix this do the following:

1. make sure that any change you made to the files on `~/projects/batch4-students`  (that you want to not lose) is saved in your `~/projects/batch4-workspace` repository (see `https://github.com/LDSSA/batch4-students#updates-to-learning-units` for how to do this), and if you don't want to keep the changes you made to these files, just continue on to the next step
2. go to the `~/projects/batch4-students` folder and run:

    ```bash
    cd ~/projects/batch4-students
    git stash
    ```

3. now you can pull from the `batch4-students` repository:

    ```bash
    git pull
    ```

#### When I try to open `jupyter notebook` I get the error

```bash
migs-MBP% jupyter notebook
zsh: command not found: jupyter
```

Before opening `jupyter notebook` activate your virtual environment:

```bash
source ~/.virtualenvs/slu00/bin/activate
```

#### When I use the `cp` command the `>` sign appears and the command does not execute

```bash
cp -r ~/projects/batch4-students/“Week 0" batch4-workspace
>
```

Make sure to use this type of quotes `"` and not these ones `“`.

#### My problem is not listed here what should I do?

If the above steps didn't solve the problem for you, please contact us on Slack or if you are not on slack, [open an issue](https://guides.github.com/features/issues/)

### Other

If your problem doesn't fit in any  of the previous categories head over to
slack and ask.
Someone will surely point you in the right direction.

If you're looking for some specific part of our organization head over to the
[Member Directory](https://github.com/LDSSA/wiki/wiki/Member-Directory)
and search for the area of responsibility you're looking for.
