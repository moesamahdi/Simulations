var canvas = document.querySelector('#simcanvas');
var c = canvas.getContext('2d');
var pause_sim = false;
var random_vel = true;
var counter = 0;
////// FUNCTIONS //////
// move function takes current body index, the body itself and the bodies list
function move(i,b,bodys){
	var cur_s = b.getposition();
	var new_s = [0,0];
	var cur_v = b.getvelocity();
	var new_v = [0,0];
	//var acc_list = [];
	var new_a = [0,0];
	//Calculated acceleration
	for(var j = 0; j < bodys.length; j++){
		if(j != i){new_a = add(new_a,b.cal_acc(bodys[j]));}
	}
	b.setacceleration(new_a);
	//update velocity
	new_v = add(cur_v,scale(time_int,new_a));
	b.setvelocity(new_v);
	//update position
	new_s = add(cur_s,scale(time_int,new_v))
	b.setposition(new_s);
}

function draw(body){
	var color = body.getcolor();
	var s = body.getposition();
	var radi = body.getradius();//20*Math.cbrt((3*body.getmass())/(4*Math.PI*0.5));
	c.beginPath();
	c.arc(s[0],s[1],radi,0,2*Math.PI);
	c.stroke();
	c.fillStyle = color;
	c.fill();
	c.closePath();
}

function update(){
	c.clearRect(0,0,canvas.width,canvas.height);
	for(var n = 0; n < steps; n++){
		for(var i = 0; i < bodies.length; i++){
			move(i,bodies[i],bodies);
		}
	}
	for(var i = 0; i < bodies.length; i++){
		draw(bodies[i]);
	}
	counter++;
	if(counter == 30){
		console.log(scale(1/300,sub(bodies[1].getposition(),bodies[0].getposition())));
		console.log(scale(1/300,sub(bodies[1].getvelocity(),bodies[0].getvelocity())));
	}
	// Each frame is 16ms
	if(pause_sim == false){
		window.requestAnimationFrame(update);
	}
}
/// PAUSE AND PLAY SIMULATION ///
function pause_play(){
	if(pause_sim == false){
		pause_sim = true;
		document.querySelector('#pauseplay').src = 'Images/play.png';
	}
	else{
		pause_sim = false;
		document.querySelector('#pauseplay').src = 'Images/pause.png';
		update();
	}
}

/////// VECTOR ALGEBRA ///////
function add(arr1,arr2){
	new_arr = [0,0];
	new_arr[0] = arr1[0] + arr2[0];
	new_arr[1] = arr1[1] + arr2[1];
	return new_arr;
}
function sub(arr1,arr2){
	new_arr = [0,0];
	new_arr[0] = arr1[0] - arr2[0];
	new_arr[1] = arr1[1] - arr2[1];
	return new_arr;
}
function scale(scalar,arr){
	new_arr = [0,0];
	new_arr[0] = scalar*arr[0];
	new_arr[1] = scalar*arr[1];
	return new_arr;
}
// RANDOM VELOCITY
function randvel(){
	var randx = 10*( (Math.random() - 0.5) );
	var randy = 10*( (Math.random() - 0.5) );
	document.querySelector('#velx').value = randx;
	document.querySelector('#vely').value = randy;
}

////// BODY OBJECT //////
function body(mass,pos,vel){
	this.col;
	this.m = mass;
	this.rad;
	this.s = pos;
	this.v = vel;
	this.a = [0,0];
	this.t = 0;
	
	this.getcolor = function(){return this.col;}
	this.setcolor = function(colour){this.col = colour;}
	this.getmass = function(){return this.m;}
	this.setmass = function(mas){this.m = mas;}
	this.getradius = function(){return this.rad;}
	this.setradius = function(radi){this.rad = radi;}
	this.getposition = function(){return this.s;}
	this.setposition = function(posi){this.s = posi;}
	this.getvelocity = function(){return this.v;}
	this.setvelocity = function(velo){this.v = velo;}
	this.cal_acc = function(body){
		var scalar = -G*body.getmass(); 
		var r = Math.sqrt( Math.pow(this.s[0] - body.getposition()[0],2)
						 + Math.pow(this.s[1] - body.getposition()[1],2) );

		return scale(scalar/Math.pow(r,3),sub(this.s,body.getposition()));
	}
	this.setacceleration = function(accel){this.a = accel;}
}
// NEW BODY //
function new_body(){
	var sim = document.querySelector('.sim');
	var simc = document.querySelector('#simcanvas');

	var colour = document.querySelector('#colour').value;
	var mass = document.querySelector('#mass').value * Math.pow(10,22);

	var pos_x = event.clientX - simc.offsetLeft + sim.scrollLeft + document.documentElement.scrollLeft;
	var pos_y = event.clientY - simc.offsetTop + sim.scrollTop + document.documentElement.scrollTop;
	var mouse_pos = [pos_x,pos_y];

	var vel_x = document.querySelector('#velx').value * Math.pow(10,-5);
	var vel_y = document.querySelector('#vely').value * Math.pow(10,-5);
	var vel = [vel_x,-vel_y];
	console.log(vel);
	bodies.push( new body(mass,mouse_pos,vel) );
	
	bodies[bodies.length-1].setradius(Math.min( (mass*Math.pow(10,-22))+3 ,20));
	bodies[bodies.length-1].setcolor(colour);
	draw(bodies[bodies.length-1]);
}

// INITIAL CONDITIONS //
function initial(){
	bodies = [];
	G = 5.38*Math.pow(10,-37);
	steps = 10;
	time_int = 24*3600/steps;
	var in_con = {
		b1: {
			mass: 1.989*Math.pow(10,30),
			pos: [1000,850],
 			vel: [0,0]
		},
		b2: {
			mass: 5.972*Math.pow(10,24),
 			pos: [(1000+294.78),(850+48.7985)],
 			vel: [-1.03*Math.pow(10,-5),-5.87*Math.pow(10,-5)]
		}
	}
	// Array of particles
	bodies.push(new body(in_con.b1.mass,in_con.b1.pos,in_con.b1.vel))
	bodies.push(new body(in_con.b2.mass,in_con.b2.pos,in_con.b2.vel))
	bodies[0].setradius(50);
	bodies[0].setcolor('#ffff00');
	bodies[1].setradius(20);
	bodies[1].setcolor('#5d8aa8');
	var simwindow = document.querySelector('.sim');
	simwindow.scrollTop = 620;
	simwindow.scrollLeft = 590;
	// Draw particles and start simulation
	for(var i = 0; i < bodies.length; i++){
		draw(bodies[i]);
	}

	update();
}
////// RUN CODE //////
initial();
document.querySelector('#simcanvas').addEventListener('click',new_body);
