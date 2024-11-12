# cron-crawler-template

This is a template allowing you to run crawler cron jobs with GitHub Action and send email notification to yourself.

Crawlers should be defined within [jobs](./jobs) directory and extend abstract class [AbstractJob](./src/job.py).

There are 2 job sample files:

- [jobs/worldtime.py](./jobs/worldtime.py)
- [jobs/daily/worldtime2.py](./jobs/daily/worldtime2.py)

jobs can be placed in nested folders under [jobs](./jobs) folder.

The class name for all jobs must be `Job`. 

Non `.py` files can also be placed under [jobs](./jobs) folder but will be ignored, you may add template files if you want.

Helper functions can also be defined in separate files under [jobs](./jobs) folder. All files with a `Job` class will be loaded and the `Job` class will be run.

Note that the initializer of a `Job` class doesn't take any arguments, so define all variables you need within the class.

You can have a subfolder storing daily jobs, another one storing weekly jobs, etc.

# How the jobs are run?

## Run all jobs

[main.py](./main.py) will run all jobs under [jobs](./jobs) directory.

```bash
python main.py
```

## Run a single file or a folder of files

```bash
python run.py --modules ./jobs/daily            # run all jobs under ./jobs/daily folder
python run.py --modules ./jobs/worldtime.py     # run a single job
```

# GitHub Action

[all-jobs-daily.yml](./.github/workflows/all-jobs-daily.yml) is a sample github workflow for running [main.py](./main.py) (all jobs) daily.

[report-time-daily.yml](./.github/workflows/report-time-daily.yml) is a sample github workflow for running [run.py](./run.py) on a folder daily.

# Email Notification

To send email notifications, the code is in file [./src/notifier.email_notifier.py](./src/notifier/email_notifier.py).

Sample usage can be found in the sample job file [jobs/worldtime.py](https://github.com/HuakunShen/cron-crawler-template/blob/master/jobs/worldtime.py#L24).

In order for email notification to work, you must provide your email server address, email addresses and email password.

You can put all non-secret environment variables in [public.env](./public.env).

My `MAIL_SERVER` variable is defined in [public.env](./public.env).

Secret environment variables are not recommended to be pushed to GitHub.

When developing locally, you can create a `.env` file to store secret environment variables.

The following 3 variables should be defined in order for email notification to work

- `EMAIL_PASSWORD`
- `FROM_EMAIL_ADDRESS`
- `TO_EMAIL_ADDRESS`

When running cron job with github action, you may add the variables to GitHub Action Secrets, and don't for forget to declare these varaibles in the workflow yaml files. 

For example,

```yaml
...
jobs:
  crawl:
    steps:
      - name: Run the main crawler
        env:
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          FROM_EMAIL_ADDRESS: ${{ secrets.FROM_EMAIL_ADDRESS }}
          TO_EMAIL_ADDRESS: ${{ secrets.TO_EMAIL_ADDRESS }}
        run: python main.py
```

# Add Your Custom Features

You may add any custom features to for your crawler. This is just a template.

All source code can be found in [./src](./src) folder. If you need to add an SMS notifier, modify the email notifier or add a email html template, just add/modify the files in `src/notifier`.

Note that if you add any secret environment variables, use `.env` when developing locally and GitHub Action Secrets when running as a GitHub Workflow, and don't forget to declare the variables used in your GitHub Workflow yaml files.

If any other python packages were used, don't forget to add the dependencies to [requirements.txt](./requirements.txt).

When code is pushed to `develop` branch, the GitHub Workflows (the samples I provided) will be run, otherwise they will follow the cron schedule defined.