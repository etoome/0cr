<script lang="ts">
	import { goto } from '$app/navigation';
	import * as store from '$lib/store';
	import * as api from '$lib/api';
	import Reveal from '../components/Reveal.svelte';
	import { onDestroy } from 'svelte';

	const unsubscribe = store.user.subscribe(async (u) => {
		if (u !== null) {
			goto(`/jeu`);
		}
	});
	onDestroy(unsubscribe);

	let input: HTMLInputElement;

	async function onSubmit() {
		const key = input.value;

		const logged = await api.login(key);

		if (logged) {
			goto(`/jeu`);
		} else {
			input.value = '';
		}
	}
</script>

<div class="flex flex-col justify-center items-center h-full gap-20">
	<div>
		<div class=" text-accent text-4xl font-bold text-center flex justify-center items-center">
			<Reveal textin="联系" textout="Connexion" />
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
				<a href="/inscription">
					<Reveal textin="登记" textout="inscription" />
				</a>
			</div>
		</div>
	</div>
	<div class="bg-white shadow p-9 rounded-md">
		<form on:submit|preventDefault={onSubmit}>
			<div class="flex flex-col items-center gap-6">
				<div class="flex flex-col gap-1">
					<label for="key" class="text-accent font-medium w-32 h-6">
						<Reveal textin="钥匙" textout="Clé" />
					</label>

					<input
						bind:this={input}
						type="text"
						id="key"
						name="key"
						class="outline-none p-1 rounded-md bg-white border-2 border-accent focus:border-primary border-opacity-30"
					/>
				</div>

				<button type="submit" class="w-full h-9 font-semibold bg-primary text-white rounded-md">
					<Reveal textin="联系" textout="Connexion" />
				</button>
			</div>
		</form>
	</div>
</div>
