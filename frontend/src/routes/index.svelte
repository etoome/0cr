<script lang="ts">
	import * as store from '$lib/store';
	import Reveal from '../components/Reveal.svelte';

	store.reset();
</script>

<div class="flex flex-col justify-center items-center h-full gap-6">
	<a href="/inscription" class="text-3xl font-semibold text-primary ">
		<Reveal textin="登记" textout="Inscription" />
	</a>
	<div
		class="text-accent opacity-50 text-lg font-bold text-center flex justify-center items-center"
	>
		<Reveal textin="或" textout="ou" />
	</div>
	<a href="/connexion" class="text-3xl font-semibold text-primary ">
		<Reveal textin="联系" textout="Connexion" />
	</a>
</div>
