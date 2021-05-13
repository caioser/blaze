function nwlist() {
	let list = document.querySelectorAll('tr'); // lista de nós com cada linha da planilha
	let nwlist = []; // para primeiro nó de cada linha
	let arr = []; // para valor de cada primeiro nó de cada linha
	for(var value of list.values()) {
		nwlist.push(value.querySelector('td')); // pega o primeiro nó de cada linha
	}
	for (let i=1; i<nwlist.length; i++) {
		arr.push(parseFloat(nwlist[i].innerHTML)) // pega o valor(de string pra float) de cada primeiro nó(td) de cada linha(tr)
	}
	return arr;
}

function nwordered(nw) {
	return nw.sort((a,b)=>a-b);
}

function count_duplicate(a){
 let counts = {}

 for(let i =0; i < a.length; i++){ 
     if (counts[a[i]]){
     counts[a[i]] += 1
     } else {
     counts[a[i]] = 1
     }
    }  
    for (let prop in counts){
        if (counts[prop] >= 2){
            console.log(prop + " counted: " + counts[prop] + " times.")
        }
    }
  console.log(counts)
}

function percentil_duplicate(a) {
	let proportions = {
		'zeros': 0,
		'até 1.5': 0,
		'até 2': 0,
		'acima de 2': 0
	};
	
	for (let i=0; i<a.length; i++){
		if (a[i] <= 1) {
			proportions.zeros += 1; 
		} else if (a[i] < 1.6) {
			proportions['até 1.5'] += 1;
		} else if (a[i] < 2) {
			proportions['até 2'] += 1;
		} else {
			proportions['acima de 2'] += 1;
		}
	}
	let total = 0;
	let text = `Last factor ${a[0]}
From ${a.length} entries:

`;
	for (let prop in proportions){
		proportions[prop] = (proportions[prop] / a.length)*100;
		text += `${prop}: ${proportions[prop].toFixed(2)}%
`;
	}
	for (let prop in proportions){
		total += proportions[prop];
	}
	text += `
total: ${total.toFixed(2)}%`;
	return text;
}

function doo() {
	let a = nwlist();
	console.log(percentil_duplicate(a))
}
