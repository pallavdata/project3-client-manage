var updatedate = new Date()
var minuts = ""
if (updatedate.getMinutes() < 10){
  minuts="0"+updatedate.getMinutes();
}
else{
  minuts=updatedate.getMinutes();
}
const dateControl = document.querySelector('#id_From');
dateControl.value = updatedate.getFullYear()+"-"+updatedate.getMonth()+"-"+updatedate.getDate()+"T"+updatedate.getHours()+":"+minuts+":00";
dateControl.max = (updatedate.getFullYear()+5)+"-"+updatedate.getMonth()+"-"+updatedate.getDate()+"T"+updatedate.getHours()+":"+minuts;
dateControl.min = (updatedate.getFullYear())+"-"+updatedate.getMonth()+"-"+updatedate.getDate()+"T"+updatedate.getHours()+":"+minuts;

const dateControl2 = document.querySelector('#id_to');
dateControl2.value = updatedate.getFullYear()+"-"+updatedate.getMonth()+"-"+(updatedate.getDate()+1)+"T"+updatedate.getHours()+":"+minuts+":00";
dateControl2.max = (updatedate.getFullYear()+5)+"-"+updatedate.getMonth()+"-"+updatedate.getDate()+"T"+updatedate.getHours()+":"+minuts;
dateControl2.min = (updatedate.getFullYear())+"-"+updatedate.getMonth()+"-"+updatedate.getDate()+"T"+updatedate.getHours()+":"+minuts;
