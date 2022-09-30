<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { afterNavigate } from '$app/navigation';
	import * as store from '$lib/store';
	import type { User } from '../types/store';
	import { fade } from 'svelte/transition';

	let leaderboard: boolean = false;
	afterNavigate(() => {
		leaderboard = $page.url.pathname === '/classement';
	});

	let user: User | null = null;
	store.user.subscribe((u) => {
		user = u;
	});
</script>

<svelte:head>
	<title>0CR{user !== null ? ` - ${user.username}` : ''}</title>
</svelte:head>

<header class="absolute top-0 w-full py-3 px-4 flex justify-between select-none">
	<a href="/" class="text-3xl sm:text-2xl font-bold text-primary hover:text-secondary">介</a>

	<div>
		{#if user !== null}
			<div transition:fade class="blur hover:blur-0 transition-all">
				<span class="font-semibold text-accent select-text">
					{user.key}
				</span>
			</div>
		{/if}
	</div>

	<a
		href={leaderboard ? (user !== null ? `/jeu` : `/`) : `/classement`}
		class="h-6 w-6 text-3xl sm:text-2xl font-bold hover:text-secondary"
		class:text-primary={!leaderboard}
		class:text-accent={leaderboard}
	>
		三
	</a>
</header>

<main id="pattern" class="h-screen bg-background select-none">
	<slot />
</main>

<style>
	#pattern {
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'%3E%3Cpath fill='%239C92AC' fill-opacity='0.4' d='M1 3h1v1H1V3zm2-2h1v1H3V1z'%3E%3C/path%3E%3C/svg%3E");
	}
</style>
