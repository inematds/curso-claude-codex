// checa-js.js — extrai os <script> inline de cada página e tenta compilar; aponta erro de sintaxe (ex.: apóstrofo em string traduzida)
const fs=require('fs'),path=require('path'),vm=require('vm');
const files=process.argv.slice(2);let bad=0;
for(const f of files){const h=fs.readFileSync(f,'utf8');const re=/<script(?![^>]*src)(?![^>]*type="application\/json")[^>]*>([\s\S]*?)<\/script>/g;let m,i=0;
  while((m=re.exec(h))){i++;try{new vm.Script(m[1],{filename:f+'#script'+i})}catch(e){bad++;const line=(e.stack.match(/#script\d+:(\d+)/)||[])[1];console.log(f+' script#'+i+': '+e.message+(line?' (linha '+line+' do script)':''));}}}
console.log(bad?bad+' erro(s)':'todos os scripts inline compilam');process.exit(bad?1:0);
