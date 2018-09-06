editor = document.getElementById("editor");
function u_repl(str,old_,new_)
{
  return str.split(old_).join(new_);
}
function expand(c)
{
    var start = c.selectionStart,
    	end = c.selectionEnd;
    c.value = u_repl(c.value,"hsl;","`hsl(${},99%,50%)`;");
    c.value = u_repl(c.value,"hsla;","`hsla(${},99%,50%,.5)`;");
    c.value = u_repl(c.value,"x.fs=","x.fillStyle=");
    c.value = u_repl(c.value,"x.ss=","x.strokeStyle=");
    c.value = u_repl(c.value,"x.fr","x.fillRect(");
    c.value = u_repl(c.value,"x.bp;","x.beginPath();");
    c.value = u_repl(c.value,"x.fl;","x.fill();");
    c.value = u_repl(c.value,"x.sk;","x.stroke();");
    c.value = u_repl(c.value,"x.sr","x.strokeRect(");
    c.value = u_repl(c.value,"clear;","c.width^=0;");
    c.value = u_repl(c.value,"middle;","x.translate(960,540);");
    c.value = u_repl(c.value,"1time","t?0:event;");
    c.value = u_repl(c.value,"x.gcop=","x.globalCompositeOperation=");
    c.value = u_repl(c.value,"x.dri","x.drawImage(c,0,0)");
    c.value = u_repl(c.value,"m.ab","Math.abs()");
    c.value = u_repl(c.value,"m.rn","Math.random()");
    c.value = u_repl(c.value,"..rb",Math.random()<0.5?'1':'0');
    c.value = u_repl(c.value,"..for","for(i=0;i++<10;)");
    c.value = u_repl(c.value,"gr1","α");
    c.value = u_repl(c.value,"gr2","β");
    c.value = u_repl(c.value,"gr3","θ");
    c.value = u_repl(c.value,"gr4","τ");
    c.value = u_repl(c.value,"gr5","λ");
    c.value = u_repl(c.value,";\n",";");
    c.value = u_repl(c.value,"  ",",");
    c.setSelectionRange(start, end);
}
setInterval(function() { expand(editor); },50);
