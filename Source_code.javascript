
`/**Borrowed code from https://webapps.stackexchange.com/questions/19513/how-to-delete-all-events-on-many-dates-all-at-once-but-not-the-whole-calendar-in */
function delete_events(){
var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
var matrix = spreadsheet.getSheetByName("Matrix");
var calendarId = matrix.getRange("I5").getValue();
//var eventCal = CalendarApp.getCalendarById(calendarId);
var fromDate = new Date(matrix.getRange("G25").getValue());
var toDate = new Date(matrix.getRange("G26").getValue());

var ui = SpreadsheetApp.getUi();

var result = ui.alert(
'Are you sure that you want to delete all events within the set date range?',
'Note: Only events created by this spreadsheet will be deleted.',
ui.ButtonSet.YES_NO);

// delete from fromDate to endDate
if (result == ui.Button.YES) {
var calendar = CalendarApp.getCalendarById(calendarId);;
var events = calendar.getEvents(fromDate, toDate);
for(var i=0; i<events.length;i++){
var ev = events[i];
if(ev.getDescription() === "class"){
Logger.log(ev.getTitle()); // show event name in log
ev.deleteEvent();
}
}
} else {
// User clicked "No" or X in the alert window.
return;
}
}

function myFunction() {

//Task 1: Figure out how to pull data from separate spreadsheets from sheets
//Task 2: Figure out how to do the date continuation in java script
//Task 3: Figure out how to do format string in javascript

/** Accessing the spreadsheet and the calendar */
var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
var matrix = spreadsheet.getSheetByName("Matrix");
var ms = spreadsheet.getSheetByName("MS");
var holidays = spreadsheet.getSheetByName("Holidays");
var deletes = spreadsheet.getSheetByName("DELETE");

Logger.log(spreadsheet.getName());
Logger.log(matrix.getName());
Logger.log(ms.getName());
Logger.log(holidays.getName());

var calendarId = matrix.getRange("I5").getValue();
var eventCal = CalendarApp.getCalendarById(calendarId);

/** Accessing the data from spreadsheet MS */
var classes = ms.getRange("A4:F11").getValues();

//Accessing start and end dates
var currentDateFetch = matrix.getRange("F8").getValue();
var endDateFetch = matrix.getRange("I8").getValue();
var currentDate = new Date(currentDateFetch);
var endDate = new Date(endDateFetch);

//difference in days
var difference_In_Time = endDate.getTime() - currentDate.getTime();
var difference_In_Days = difference_In_Time / (1000 * 3600 * 24);
Logger.log(difference_In_Days);

//Holidays
var listOfHolidaysz = holidays.getRange("A2:A50").getValues();
var listOfHolidays = [];
for(x=0; x<listOfHolidaysz.length; x++){
listOfHolidays.push(listOfHolidaysz[x].toString());
}

var dayCount = 0;
// weekCycle refers to the day of the week (i.e. Monday, Tuesday, etc.)
var weekCycle = matrix.getRange("P6").getValue();
// cycle refers to the rotation of block days (i.e. A, B, C, D)
var cycle = parseInt(matrix.getRange("P7").getValue());
Logger.log(cycle);

var deleteConfirmation = deletes.getRange("B6").getValue();
if(deleteConfirmation === "YES"){
delete_events();
}else{
while(cycle<4){ //four day cycle
if(!(dayCount < difference_In_Days)){ //total day count
break;
}else if(listOfHolidays.includes(currentDate.toDateString())){ //skipping the holidays
currentDate.setDate(currentDate.getDate()+1);
weekCycle++;
dayCount++;
}else if(parseInt(weekCycle) == 5){ //skipping the weekends
currentDate.setDate(currentDate.getDate()+2);
dayCount += 2;
weekCycle = 0;
}else{ //actual creation of events
dayCount++;
weekCycle++;
switch(cycle){
case 0:
dayA();
currentDate.setDate(currentDate.getDate()+1);
cycle++;
break;
case 1:
dayB();
currentDate.setDate(currentDate.getDate()+1);
cycle++;
break;
case 2:
dayC();
currentDate.setDate(currentDate.getDate()+1);
cycle++;
break;
case 3:
dayD();
currentDate.setDate(currentDate.getDate()+1);
cycle=0;
break;
}
}
}
}
var deletes = spreadsheet.getSheetByName("DELETE");
var cell = deletes.getRange("B6").getValue();
cell.toString().replace("YES","NO");
//I want to create day A, day B, day C, day D separate classes
function dayA(){
for(x=0; x<8; x++){
var s1Class = classes[x]; //accessing the rows of the matrix

  var start = new Date(currentDate.toDateString() + " " + String(s1Class[0]));
  var end = new Date(currentDate.toDateString() + " " + String(s1Class[1]));
  var a = s1Class[2];
  Logger.log(a);
  if (!(a.length === 0)) {
    eventCal.createEvent(a, start, end, {description: "~class~"});
  }
}
}

function dayB(){
for(x=0; x<8; x++){
var s1Class = classes[x]; //accessing the rows of the matrix

  var start = new Date(currentDate.toDateString() + " " + String(s1Class[0]));
  var end = new Date(currentDate.toDateString() + " " + String(s1Class[1]));
  var b = s1Class[3];
  Logger.log(b);
  if (!(b.length === 0)) {
    eventCal.createEvent(b, start, end, {description: "~class~"});
  }
}
}

function dayC(){
for(x=0; x<8; x++){
var s1Class = classes[x]; //accessing the rows of the matrix

  var start = new Date(currentDate.toDateString() + " " + String(s1Class[0]));
  var end = new Date(currentDate.toDateString() + " " + String(s1Class[1]));
  var c = s1Class[4];
  Logger.log(c);
  if (!(c.length === 0)) {
    eventCal.createEvent(c, start, end,{description: "~class~"});
  }
}
}

function dayD(){ //parameters to be the semester.
for(x=0; x<8; x++){
var s1Class = classes[x]; //accessing the rows of the matrix

  var start = new Date(currentDate.toDateString() + " " + String(s1Class[0]));
  var end = new Date(currentDate.toDateString() + " " + String(s1Class[1]));
  var d = s1Class[5];
  Logger.log(d);
  if (!(d.length === 0)) {
    eventCal.createEvent(d, start, end, {description: "~class~"});
  }
}
}
/**Borrowed code from https://webapps.stackexchange.com/questions/19513/how-to-delete-all-events-on-many-dates-all-at-once-but-not-the-whole-calendar-in */
function delete_events(){
var fromDate = new Date(matrix.getRange("G25").getValue());
var toDate = new Date(matrix.getRange("G26").getValue());

// delete from fromDate to endDate

var calendar = CalendarApp.getCalendarById(calendarId);;
var events = calendar.getEvents(fromDate, toDate);
for(var i=0; i<events.length;i++){
  var ev = events[i];
  if(ev.getDescription() === "~class~"){
    Logger.log(ev.getTitle()); // show event name in log
    ev.deleteEvent();
  }
}
}
}

/*creating an event and adding days to date object
var test = currentDate.toDateString() + " " + String(hs.getRange("A4").getValue());
var test2 = currentDate.toDateString() + " " + String(hs.getRange("B4").getValue());
var date1 = new Date(test);
var date2 = new Date(test2);
Logger.log(currentDate.toDateString());

//testing data
//eventCal.createEvent("TEST", date1, date2);
Logger.log(currentDate.toDateString());
currentDate.setDate(currentDate.getDate()+1);
Logger.log(listOfHolidays);
Logger.log(listOfHolidays.includes("Sat Aug 13 2022"));
*/`

