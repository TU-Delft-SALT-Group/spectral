<script lang="ts">
	import type { ModeComponentProps } from '..';
	import { Input } from '$lib/components/ui/input';

	export let fileState: ModeComponentProps<'vowel-space'>['fileStates'][0];

	let newMatchString = '';

	function addMatchString() {
		if (newMatchString == '' || fileState.matchStrings.includes(newMatchString)) return;
		console.log(fileState.matchStrings);
		fileState.matchStrings.push(newMatchString);
	}
</script>

<div>
	<h2>
		{fileState.name}
	</h2>
	<form
		on:submit={() => {
			addMatchString();
		}}
	>
		<Input bind:value={newMatchString} />
	</form>
	<ul>
		{#each fileState.matchStrings as matchString}
			<li>
				{matchString}
			</li>
		{/each}
	</ul>
</div>
