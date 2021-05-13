let qsa = (element) => document.querySelectorAll(element);
let qs = (element) => document.querySelector(element);

let a = 'div.entries span'; // element with all entrie nodes
let b = 'div.bet'; // all elements with values in column "apostas"
let c = 'div.profit'; // all elements with values in column "lucros"
let d = 'div.totals div.right span'; // specific total of bets on top right corner

function nentries() { // return the number of entries
  return qsa(a).length;
}

function listEntries() {
  let list = [];
  for (let i=0; i<nentries(); i++) {
    list.push(parseFloat(qsa(a)[i].innerText.match(/\d+/g).join(".")));
  }

  //let max = list.reduce((a, b) => Math.max(a, b));
  //let sorted = list.sort(function(a, b){return a - b});

  return list;
}

function prob() {
  let list = listEntries();
  let noDouble = ( list.filter((e)=>e<2).length / list.length ) * 100;
  let triple = ( list.filter((e)=>e>2.99).length / list.length ) * 100;

  return `n items:${list.length} -- <2:${noDouble.toFixed(2)}% -- >=3:${triple.toFixed(2)}%`
}

function man() {
  let n = nentries();
  let good = qsa(a+'.good').length;
  let bad = qsa(a+'.bad').length;
  
  return `Total:${n}  Goods:${good}(${((good/n)*100).toFixed(2)}%)    Bads:${bad}(${((bad/n)*100).toFixed(2)}%)`;
}

function listBets(dom) {
  let bets = qsa('tr.entry '+dom);
  let values = [];
  for (let i=0; i<bets.length; i++) {
      values.push(bets[i].innerText);
  }
  values = values.map((e) => {
    if (e.match(/\d+/g) == null) {
      return 0;
    } else {
      return parseFloat(e.match(/\d+/g).join("."));
    }
  });
  return values;
}

function listing() {
  let items = [b, c];
  for (let i=0; i<items.length; i++) {
    items[i] = listBets(items[i]);
  }
  return items;
}

function will() {
  let lists = listing();
  let totalBet = parseFloat(qs(d).innerText.match(/\d+/g).join("."));
  
  let apostas = lists[0].reduce((a,b)=>a+b);
  let lucro = lists[1].reduce((a,b)=>a+b);

  return `total: ${totalBet} / ${apostas.toFixed(2)} profited: ${lucro.toFixed(2)} diferença: ${(totalBet-lucro).toFixed(2)}`;
}



contador=0;
let wallet=50;
let aposta=2;
a.map(e=>{
  if(contador == 2){
    aposta *= 2;
  } else {
    aposta = 2;
  };
  wallet -= aposta;
  if(e>1.99){
    contador += 1;
    wallet += aposta*2;
    return wallet.toFixed(2)
  } else {
    contador=0;return wallet.toFixed(2)
  }
});