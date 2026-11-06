const assert=require('node:assert/strict');const {test}=require('node:test');const C=require('../dist/core.js');
const base=C.priceList(C.parseCSV('item,unit_price\nOrange,3.00\nApple,0.10'));
function run(s,p=new Map()){return C.validate(C.parseCSV('department,item,quantity,sale_total\n'+s),base,p);}
test('integer cents avoid floating-point mismatch',()=>assert.equal(run('Grocery,Apple,3,0.30')[0].valid,true));
test('one-cent difference is flagged',()=>assert.equal(run('Grocery,Orange,3,8.99')[0].issue,'Price mismatch'));
test('department overrides add and replace prices',()=>{const p=C.priceList(C.parseCSV('department,item,unit_price\nProduce,Carrot,2.50\nProduce,Orange,2.00'),true);assert.equal(run('Produce,Carrot,2,5.00',p)[0].valid,true);assert.equal(run('Produce,Orange,3,6.00',p)[0].valid,true);assert.equal(run('Grocery,Carrot,2,5.00',p)[0].issue,'Unknown item');});
test('invalid quantities and amounts are rejected',()=>{for(const q of ['-1','0','1.5','abc'])assert.equal(run('Grocery,Orange,'+q+',3.00')[0].issue,'Invalid quantity');for(const n of ['NaN','-3.00','3.001','Infinity'])assert.equal(run('Grocery,Orange,1,'+n)[0].issue,'Invalid amount');});
test('missing department is flagged',()=>assert.equal(run(',Orange,1,3.00')[0].issue,'Missing field'));
test('only valid rows contribute to department and overall totals',()=>{const s=C.summarize(run('A,Orange,2,6.00\nA,Orange,1,2.00\nB,Apple,3,0.30'));assert.equal(s.revenue,630);assert.equal(s.valid,2);assert.equal(s.flagged,1);assert.equal(s.departments[0].revenue,600);});
test('quoted commas, multiline cells, escaped quotes and BOM parse',()=>{const p=C.parseCSV('\uFEFFdepartment,item,quantity,sale_total\r\nA,"Apple, red",1,2.00\r\nB,"a""b\nc",2,3.00\r\n');assert.equal(p.rows[0].item,'Apple, red');assert.equal(p.rows[1].item,'a"b\nc');});
test('malformed files fail without partial results',()=>{for(const x of ['a,a\n1,2','a,b\n1','a,b\n"bad,2','a,b\n"a"x,2'])assert.throws(()=>C.parseCSV(x));assert.throws(()=>run('A,Orange,1,3.00\nA,Orange,1'));assert.throws(()=>C.priceList(C.parseCSV('item,unit_price\nA,2\nA,3')));});
test('money inputs are strict and safe',()=>{assert.equal(C.cents('1.2'),120);assert.equal(C.cents('0.01'),1);assert.equal(C.cents('1e3'),null);assert.equal(C.cents('999999999999999'),null);assert.equal(run('A,Orange,9007199254740991,3')[0].issue,'Amount too large');});
test('CSV exports neutralize formulas and escape quotes',()=>{assert.equal(C.csv([['=HYPERLINK("x")','a,b']]),'"\'=HYPERLINK(""x"")","a,b"');});
