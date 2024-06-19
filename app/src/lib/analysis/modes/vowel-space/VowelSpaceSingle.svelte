<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { generateIdFromEntropySize } from 'lucia';
	import { Button } from '$lib/components/ui/button';
	import { TrashIcon } from 'lucide-svelte';
	import type { mode } from '..';

	let {
		fileState = $bindable(),
		computedData
	}: {
		computedData: mode.ComputedData<'vowel-space'>;
		fileState: mode.FileState<'vowel-space'>;
	} = $props();

	let newMatchString = $state('');

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
		Name: {fileState.name}
	</h2>
	<form
		class="flex"
		onsubmit={() => {
			addMatchString();
		}}
	>
		<Label>New Match String</Label>
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
								class="flex h-full w-full items-center justify-center overflow-clip text-secondary-foreground opacity-80"
								>{matchString.matchString}</span
							>
						</Tooltip.Trigger>
						<Tooltip.Content>
							<p>Match String</p>
						</Tooltip.Content>
					</Tooltip.Root>
					{#if matchString.selected}
						<Tooltip.Root>
							<Tooltip.Trigger>
								<span
									class="flex h-full w-full items-center justify-center overflow-clip text-secondary-foreground opacity-80"
									>f1:{computedData?.formants
										.filter((f) => f.matchString === matchString.matchString)
										.map((f1) => f1.f1)
										.reduce((acc, curr, _, arr) => acc + curr / arr.length, 0)
										.toFixed(2)}
									f2:{computedData?.formants
										.filter((f) => f.matchString === matchString.matchString)
										.map((f2) => f2.f2)
										.reduce((acc, curr, _, arr) => acc + curr / arr.length, 0)
										.toFixed(2)}
								</span>
							</Tooltip.Trigger>
							<Tooltip.Content>
								<p>Average score of all captions matching this string</p>
							</Tooltip.Content>
						</Tooltip.Root>
					{/if}
				</div>
			</li>
		{/each}
	</ul>
</div>
