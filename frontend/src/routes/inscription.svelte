<script lang="ts">
	import { goto } from '$app/navigation';
	import * as store from '$lib/store';
	import * as api from '$lib/api';
	import Reveal from '../components/Reveal.svelte';
	import { onDestroy } from 'svelte';

	let user;
	let registered = false;
	const unsubscribe = store.user.subscribe(async (u) => {
		user = u;
		if (u !== null && registered === false) {
			goto(`/jeu`);
		}
	});
	onDestroy(unsubscribe);

	let input: HTMLInputElement;

	async function onSubmit() {
		registered = true;
		const username = input.value;
		await api.register(username);
		input.value = '';
	}

	function play() {
		goto(`/jeu`);
	}
</script>

{#if registered && user}
	<div
		class="absolute z-30 w-screen h-screen bg-accent bg-opacity-50 flex justify-center items-center"
	>
		<div
			class="bg-white rounded-md p-9 min-w-[320px] flex flex-col justify-center items-center gap-4"
		>
			<div class="p-4 flex flex-col justify-center items-center gap-8">
				<div class="text-xl">
					<Reveal textin="连接钥匙" textout="Clé de connexion" />
				</div>
				<span class="font-semibold text-accent text-xl select-text">
					{user.key}
				</span>
				<button on:click={play} class="px-4 py-2 font-semibold bg-primary text-white rounded-md"
					><Reveal textin="著名的" textout="C'est noté" /></button
				>
			</div>
		</div>
	</div>
{/if}

<div class="flex flex-col justify-center items-center h-full gap-20">
	<div>
		<div class=" text-accent text-4xl font-bold text-center flex justify-center items-center">
			<Reveal textin="登记" textout="Inscription" />
		</div>
		<div class="flex justify-center gap-1">
			<div
				class=" text-accent opacity-50 text-lg font-bold text-center flex justify-center items-center"
			>
				<Reveal textin="或" textout="ou" />
			</div>
			<div
				class=" text-primary opacity-50 text-lg font-bold text-center flex justify-center items-center"
			>
				<a href="/connexion">
					<Reveal textin="联系" textout="connexion" />
				</a>
			</div>
		</div>
	</div>
	<div class="bg-white shadow p-9 rounded-md">
		<form on:submit|preventDefault={onSubmit}>
			<div class="flex flex-col items-center gap-6">
				<div class="flex flex-col gap-1">
					<label for="username" class="text-accent font-medium w-32 h-6">
						<Reveal textin="用户名" textout="Nom d'utilisateur" />
					</label>

					<input
						bind:this={input}
						type="text"
						id="username"
						name="username"
						minlength="3"
						maxlength="24"
						class="outline-none p-1 rounded-md bg-white border-2 border-accent focus:border-primary border-opacity-30"
					/>
				</div>

				<button type="submit" class="w-full h-9 font-semibold bg-primary text-white rounded-md">
					<Reveal textin="登记" textout="S'inscrire" />
				</button>
			</div>
		</form>
	</div>
</div>
