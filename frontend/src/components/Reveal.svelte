<script lang="ts">
	export let textin: string;
	export let textout: string;

	let over: boolean = false;
</script>

<div
	on:mouseenter={() => {
		over = true;
	}}
	on:mouseleave={() => {
		over = false;
	}}
>
	{#if over}
		{textout}
	{:else}
		{textin}
	{/if}
</div>
