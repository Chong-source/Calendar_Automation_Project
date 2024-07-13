# Calendar_Automation_Project (About)
This is a documentation of the Calendar Automation Project that <a href="https://github.com/Chong-source">@Chong-source</a> completed during his senior year of high school. He used javascript as the language and used the API platform that Google provided to create this program. The code autopopulates Google Calendar with events that follow a 4-day rotation.

*More background information*:  
This project started from a desire for teachers and students at a high school to be able to create repeating events on Google Calendar. By default, Google Calendar does allow users to create repeating events, however, it is not possible to create repeating events that run on a waterfall schedule with Google Calendar.  
  
To clarify: The target school's schedules run on a 4 day rotation and then reset (Day A, Day B, Day C, Day D). If there is a holiday, the pattern is paused, and then after the holiday the rotation continues with the next day in the pattern. A set of 4 weeks might look something like this:

<br>


| Week #  | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| ------- |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | A | B | C | D | A | - | - |
| 2 | B | C | D | A | B | - | - |
| 3 | C | Holiday | D | A | B | - | - |
| 4 | C | D | A | B | C | - | - |

<br>

In updating this project, the hope is to also allow functionality for waterfall schedules of other lengths (i.e. 2 day, 3 day, 5 day, or more). This will allow for other organizations to make use of this project to help them with their own unique scheduling needs.
<br>
<br>

## Plans for updating this project:
### Definite plans:
- Rewrite with Python and use Google Calendar API.
- Allow script to be run from the command line.
- Make use of CSV files instead of Google Sheets.

### Possible future updates:
- Create a GUI for the scheduler.
<br>
<br>

## List of requirements for a Python command line version:
1. The standard waterfall schedule needs to be defined.
2. Allow for other schedules to be easily created so that the standard waterfall time schedule can be altered as needed.
3. It must be possible to populate calendars with events (based on a given time schedule) both individually and in bulk. Single or many events should be able to be created for just one calendar, or for many calendars at once.
3. It must be possible to delete events both individually and in bulk. Single or many events should be able to be deleted from just one calendar, or from many calendars at once.
3. Allow date ranges to be specified for when calendars should be populated.
4. The program needs to know when holidays are so that they can be skipped.
5. A preview of a schedule should be displayed before sending events to Google Calendar.
