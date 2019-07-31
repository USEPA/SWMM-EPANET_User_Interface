window.onload= resizeSplitWndw;
window.onresize= resizeSplitWndw;
window.onbeforeprint= set_to_print;
window.onafterprint= reset_form;

function resizeSplitWndw(){

var onsr= document.all.item("nsr");
var omainbody= document.all.item("mainbody");

document.all.mainbody.style.width= 0; //IE6 reload bug
if (omainbody ==null) return;
if (onsr != null){
document.all.mainbody.style.overflow= "auto";
document.all.nsr.style.width= document.body.offsetWidth-4;
document.all.mainbody.style.width= document.body.offsetWidth-4;
document.all.mainbody.style.top= document.all.nsr.offsetHeight;
if (document.body.offsetHeight > document.all.nsr.offsetHeight)
document.all.mainbody.style.height= document.body.offsetHeight - document.all.nsr.offsetHeight-4;
else document.all.mainbody.style.height=0;
}
}

function set_to_print(){

var i;
if (window.mainbody)document.all.mainbody.style.height = "auto";

for (i=0; i < document.all.length; i++){
if (document.all[i].tagName == "BODY") {
document.all[i].scroll = "auto";
}
if (document.all[i].tagName == "A") {
document.all[i].outerHTML = "<a href=''>" + document.all[i].innerHTML + "</a>";
}
}
}

function reset_form(){

document.location.reload();
}