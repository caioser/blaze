function crashPointFromHash(hash) {
  const divisible = (hash, mod) => {
      console.log(`"divisible()" init whith ${hash} and ${mod}`);
    // So ABCDEFGHIJ should be chunked like  AB CDEF GHIJ
    let val = 0;
      console.log(`"let val": ${typeof(val)} ${val}`);
    let o = hash.length % 4;
      console.log(`"let o" hash length % 4: ${typeof(o)} ${o}`)
      console.log(`init for`)
    for (let i = o > 0 ? o - 4 : 0; i < hash.length; i += 4) {
      console.log(`
i = ${i} < ${hash.length} => hash.length
val = ${val}
((val << 16) + parseInt(hash.substring(i, i+4), 16)) % mod;
( ${val << 16} + parseInt(${hash.substring(i, i+4)}, 16)) % ${mod};
( ${val << 16} + ${parseInt(hash.substring(i, i+4), 16)}) % ${mod};
${(val << 16) + parseInt(hash.substring(i, i+4), 16)} % ${mod};
${((val << 16) + parseInt(hash.substring(i, i+4), 16)) % mod};
`);
      val = ((val << 16) + parseInt(hash.substring(i, i+4), 16)) % mod;
      console.log(val)
    }
      console.log(`val === 0: ${val === 0}`)
    val === 0 ? console.log(`Returned True: Ends here with 0`) : console.log(`Returned False: Continue script...`);
    return val === 0;
  };

  /* from here https://medium.com/@blazedev/blaze-com-multiplayer-provably-fair-implementation-ab2d35c013e0
  used 1 of 20 games the game crashes instantly.
  if (divisible(hash, 20)) */

  /* from here https://codesandbox.io/s/o5orm2mmrq?file=/src/index.js
  used 1 of 15, tested for caio in 2021-05-11-21-26-22 */
  console.log(`BEGIN
check IF divisible(hash, 15) return TRUE`);
  if (divisible(hash, 15))
    return 0;

  // Use the most significant 52-bit from the hash to calculate the crash point
  let h = parseInt(hash.slice(0,52/4),16);
  let e = Math.pow(2,52);

  console.log(`
let h
parseInt(hash.slice(0,52/4),16);
parseInt(${hash.slice(0,52/4)},16);
${parseInt(hash.slice(0,52/4),16)};

let e
Math.pow(2,52);
${Math.pow(2,52)};

proportion h/e
${(h/e)*100} %
${((h/e)*100).toFixed(2)} %

return
(Math.floor((100 * e - h) / (e - h)) / 100).toFixed(2);
(Math.floor(${100*e-h} / ${e-h}) / 100).toFixed(2);
(${Math.floor( (100*e-h)/(e-h) )} / 100).toFixed(2);
(${Math.floor( (100*e-h)/(e-h) ) / 100}).toFixed(2);
${(Math.floor( (100*e-h)/(e-h) ) / 100).toFixed(2)};`);

  return (Math.floor((100 * e - h) / (e - h)) / 100).toFixed(2);
};