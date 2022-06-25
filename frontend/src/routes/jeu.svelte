<script lang="ts">
	import { goto } from '$app/navigation';
	import * as api from '$lib/api';
	import * as store from '$lib/store';
	import Draw from '../components/Draw.svelte';
	import type { Game } from 'src/types/store';
	import { onDestroy } from 'svelte';
	import Reveal from '../components/Reveal.svelte';

	const unsubscribe = store.user.subscribe(async (u) => {
		if (u === null) {
			goto(`/`);
		}
	});
	onDestroy(unsubscribe);

	let game: Game | null = null;
	store.game.subscribe((g) => {
		game = g;
	});

	let state: 'start' | 'playing' | 'computing' | 'score' = 'start';

	async function start() {
		await api.newGame();
		play();
	}

	let canvasClear: () => void;
	let canvastoDataURL: () => string;

	let hint: boolean = true;
	function play() {
		hint = true;
		state = 'playing';
		setTimeout(() => {
			hint = false;
		}, 3000);
	}

	let oldChar: string;
	let drawing: string;
	async function submit() {
		state = 'computing';
		drawing = canvastoDataURL();
		oldChar = game.char;
		await api.play(drawing);
		state = 'score';
	}
</script>

{#if state !== 'playing'}
	<div
		class="absolute z-30 w-screen h-screen bg-accent bg-opacity-50 flex justify-center items-center"
	>
		<div
			class="bg-white rounded-md p-9 min-w-[320px] flex flex-col justify-center items-center gap-4"
		>
			{#if state === 'start'}
				<div class="p-4 flex flex-col justify-center items-center gap-8">
					<div class="text-xl">
						<Reveal textin="准备好?" textout="Prêt?" />
					</div>
					<button on:click={start} class="px-4 py-2 font-semibold bg-primary text-white rounded-md"
						><Reveal textin="我们走吧" textout="C'est parti" /></button
					>
				</div>
			{:else if state === 'computing'}
				<div class="p-32">
					<svg
						class="mr-2 w-8 h-8 animate-spin text-primary"
						viewBox="0 0 100 101"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
							fill="currentColor"
						/>
					</svg>
				</div>
			{:else if state === 'score'}
				<div class="flex flex-col justify-center items-center gap-6">
					<div class="font-bold text-4xl flex gap-2">
						{game.score}
					</div>

					<div class="flex justify-center gap-3">
						<div class="bg-white shadow rounded-md h-[175px] w-[175px]">
							<img src={drawing} alt="" />
						</div>
						<div class="flex justify-center items-center">
							<div class="text-primary text-5xl ">{game.success ? `=` : `≠`}</div>
						</div>

						<div
							class="bg-white shadow rounded-md h-[175px] w-[175px] flex justify-center items-center"
						>
							<div class="font-bold text-[160px]">
								{oldChar}
							</div>
						</div>
					</div>
				</div>
				{#if game.success}
					<button on:click={play} class="w-full h-9 font-semibold bg-primary text-white rounded-md"
						><Reveal textin="继续" textout="Continuer" /></button
					>
				{:else}
					<a
						href="/classement"
						class="w-full h-9 font-semibold bg-secondary text-white rounded-md flex justify-center items-center"
						><Reveal textin="排行" textout="Classement" /></a
					>
					<button on:click={start} class="w-full h-9 font-semibold bg-primary text-white rounded-md"
						><Reveal textin="再试一次" textout="Réessayer" /></button
					>
				{/if}
			{/if}
		</div>
	</div>
{/if}

<div class="flex justify-center items-center h-full">
	<div>
		<div class="bg-white shadow rounded-md h-[386px] w-[350px]">
			{#if state === 'playing' || state === 'score'}
				{#if state === 'playing' && hint}
					<div class="h-[350px] flex justify-center items-center">
						<div class="font-bold text-[350px]">
							{game.char}
						</div>
					</div>
				{:else}
					<div class="relative">
						<div class="absolute z-20 top-0 right-0">
							<button on:click={canvasClear} class="m-2 font-semibold text-primary">回</button>
						</div>
					</div>

					<Draw bind:clear={canvasClear} bind:toDataURL={canvastoDataURL} />

					<button
						on:click={submit}
						class="w-full h-9 font-semibold bg-primary text-white rounded-b-md"
					>
						<Reveal textin="验证" textout="Vérifier" />
					</button>
				{/if}
			{/if}
		</div>
	</div>
</div>
