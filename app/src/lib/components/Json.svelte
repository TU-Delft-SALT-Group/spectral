<!--
@component Renders a JSON object in a readable format.
-->

<script lang="ts">
	export let json: unknown;
</script>

{#if Array.isArray(json)}
	<ol>
		{#each json as item}
			<li class="pl-4">
				<svelte:self json={item}></svelte:self>
			</li>
		{/each}
	</ol>
{:else if typeof json === 'object' && json !== null}
	<ol>
		{#each Object.entries(json) as [key, value]}
			<li class="pl-4">{key}: <svelte:self json={value}></svelte:self></li>
		{/each}
	</ol>
{:else}
	{json}
{/if}
