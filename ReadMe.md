Description
===========

A simple program to store and monitor daily measured blood sugar of one person.

I made this for my wife because she have gestational diabetes during her pregnancy. That's why it's very simple. It has 3 features:

* Store measured blood sugar of 1 specific person
* After storing a blood sugar level, inform if the current level is above threshold. For the threshold, check this reference: [View of Diabetes in pregnancy: management of diabetes and its complications from preconception to the postnatal period (NG3) | British Journal of Diabetes](https://www.bjd-abcd.com/index.php/bjd/article/view/80/172)
* Back-up the blood sugar data just in case

This is created initialy just for my wife so unless I think of any other helpful features for her, there won't be any updates.

Usage
=====

* Create 3 collections in your MongoDB database: `daily_levels`, `threshold`, `users`. Create documents in `threshold` and `users` collection for the person you would like to monitor their blood sugar level
* Create a configuration json file in `configuration` directory. For reference, check file `example.json`.
* Set an environmental variable named `glucose_env` with your new configuration filename (without json extension)
* Use command `pip install requirements.txt`
* Use command `python3 daily_update.py` to store blood sugar level and to see if that level is normal or not:
    ** You can use option `-d <YYYY-MM-DD>` to store blood sugar level of a specific date. Default value without this option is today.
    ** You can use option `-k <option_number>` to specify the time you measure the blood sugar level. Without this option, a prompt will show up for you to check the option again and choose the corresponding number.
* Use command `python3 daily_backup.py` to back-up all blood sugar data of the monitored person into a `csv` file in `backup_data` directory

