<script lang="ts">
	import { onMount } from 'svelte';

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;
	let drawing: boolean = false;
	let position = {
		x: 0,
		y: 0
	};

	onMount(() => {
		ctx = canvas.getContext('2d');
	});

	function mouseStart(e: MouseEvent) {
		drawing = true;
		updatePosition({
			x: e.clientX,
			y: e.clientY
		});
	}

	function touchStart(e: TouchEvent) {
		const touch = e.touches.item(0);
		start({
			x: touch.clientX,
			y: touch.clientY
		});
	}

	function start({ x, y }: { x: number; y: number }) {
		drawing = true;
		updatePosition({ x, y });
	}

	function stop() {
		drawing = false;
	}

	function mouseDraw(e: MouseEvent) {
		draw({
			x: e.clientX,
			y: e.clientY
		});
	}

	function touchDraw(e: TouchEvent) {
		const touch = e.touches.item(0);
		draw({
			x: touch.clientX,
			y: touch.clientY
		});
	}

	function draw({ x, y }: { x: number; y: number }) {
		if (!drawing) return;

		ctx.beginPath();
		ctx.lineWidth = 20;
		ctx.lineCap = 'round';
		ctx.strokeStyle = '#000000';
		ctx.moveTo(position.x, position.y);
		updatePosition({ x, y });
		ctx.lineTo(position.x, position.y);
		ctx.stroke();
	}

	function updatePosition({ x, y }: { x: number; y: number }) {
		position = {
			x: x - canvas.offsetLeft,
			y: y - canvas.offsetTop
		};
	}

	export function clear() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
	}

	export function toDataURL() {
		return canvas.toDataURL();
	}
</script>

<canvas
	width="350"
	height="350"
	bind:this={canvas}
	on:mousedown={mouseStart}
	on:touchstart={touchStart}
	on:mousemove={mouseDraw}
	on:touchmove={touchDraw}
	on:mouseup={stop}
	on:touchend={stop}
/>
