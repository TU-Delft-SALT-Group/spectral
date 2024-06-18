<script lang="ts">
	import type { ModeComponentProps } from '..';
	import { Input } from '$lib/components/ui/input';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { generateIdFromEntropySize } from 'lucia';
	import { Button } from '$lib/components/ui/button';
	import { TrashIcon } from 'lucide-svelte';

	export let fileState: ModeComponentProps<'vowel-space'>['fileStates'][0];

	let newMatchString = '';

	function addMatchString() {
		if (
			newMatchString === '' ||
			fileState.matchStrings.map((x) => x.matchString).includes(newMatchString)
		)
			return;
		fileState.matchStrings.push({
			matchString: newMatchString,
			id: generateIdFromEntropySize(10),
			selected: true
		});
		newMatchString = '';
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
				<div class="flex w-full items-center gap-1 border-y">
					<Tooltip.Root>
						<Tooltip.Trigger>
							<Checkbox class="flex h-4 w-4 p-1" bind:checked={matchString.selected} />
						</Tooltip.Trigger>
						<Tooltip.Content>
							<p>Match on this Match String</p>
						</Tooltip.Content>
					</Tooltip.Root>
					<Tooltip.Root>
						<Tooltip.Trigger>
							<Button
								class="flex h-6 p-1"
								variant="destructive"
								on:click={() => {
									console.log('delete: ' + matchString.id);
									fileState.matchStrings = fileState.matchStrings.filter(
										(x) => x.id !== matchString.id
									);
								}}><TrashIcon class="w-4" /></Button
							>
						</Tooltip.Trigger>
						<Tooltip.Content>
							<p>Delete Match String</p>
						</Tooltip.Content>
					</Tooltip.Root>
					<Tooltip.Root>
						<Tooltip.Trigger>
							<span
								role="button"
								tabindex="0"
								class="flex h-full w-full items-center justify-center overflow-clip text-secondary-foreground opacity-80"
								>{matchString.matchString}</span
							>
						</Tooltip.Trigger>
						<Tooltip.Content>
							<p>Match String</p>
						</Tooltip.Content>
					</Tooltip.Root>
				</div>
			</li>
		{/each}
	</ul>
</div>
