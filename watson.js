function wat(inp_str)
{
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			
			var resp = (this.responseText);
			var temp=resp.replace("'","\"");
			while(resp!=temp){
				resp=temp;
				temp=resp.replace("'","\"");
			}
			resp=JSON.parse(resp);
			var values = resp[0];
			var starts = resp[1];
			var ends = resp[2];
			var the_html = "";
			for(var i=0;i<values.length;i++){
				the_html += "<div style='border:1px solid #b0b0b0;padding:5px;'>"+values[i]+"<br><br>";
				i++;
				if(i<values.length){
					the_html += "<div style='width:100px;height:2px;background-color:#a0a0a0;'><div style='background-color:#f00101;margin-left:"+(values[i]*100)+"%;height:10px;width:10px;border-radius:10px;position:relative;top:-4px;'></div></div><br>";
					the_html += "</div>";
				}
			}
			
			alert();
			document.getElementById("watson").innerHTML = the_html;
		}	
	};
	url = "http:\\localhost:8888";
	xhttp.open("POST", url, true);
	xhttp.send("data="+inp_str);
}