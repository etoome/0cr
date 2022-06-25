<script lang="ts">
	import * as api from '$lib/api';

	let leaderboard = api.leaderboard();
</script>

<div class="flex justify-center items-center h-full">
	{#await leaderboard then leaderboard}
		{#if leaderboard !== undefined}
			<ul class="h-4/5 overflow-auto">
				{#each leaderboard as { username, score, date }, i}
					<li class="m-4">
						<div class="w-80 h-20 rounded-md grid grid-cols-4 bg-white shadow">
							<div
								class={`rounded-l-md text-accent text-xl font-semibold flex justify-center items-center ${
									i === 0
										? 'bg-secondary'
										: i === 1
										? 'bg-[#a7a7ad]'
										: i === 2
										? 'bg-[#a77044]'
										: 'bg-accent bg-opacity-5'
								}`}
							>
								{score}
							</div>
							<div class="col-span-3 m-4 grid grid-rows-2">
								<div class="truncate">
									{username}
								</div>
								<div class="flex  items-end text-sm font-semibold text-accent opacity-60 truncate">
									{date.toLocaleDateString('fr-FR') || ''}
								</div>
							</div>
						</div>
					</li>
				{/each}
			</ul>
		{/if}
	{/await}
</div>
