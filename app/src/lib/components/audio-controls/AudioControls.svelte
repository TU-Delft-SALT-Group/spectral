<script lang="ts" context="module">
	let selectedStore: Writable<ControlRequirements | null> = writable(null);
	let selected: ControlRequirements | null;
	selectedStore.subscribe((update) => {
		selected = update;
	});

	const step = 0.5;

	if (browser) {
		window.addEventListener('keydown', (e: KeyboardEvent) => {
			switch (e.key) {
				case 'Escape':
					if (selected === null) return;

					if (selected.clearRegions()) return;

					selected.pause();
					selectedStore.set(null);
					break;
				case ' ':
					if (
						(e.target as HTMLTextAreaElement).tagName.toUpperCase() == 'INPUT' ||
						selected === null
					)
						return;
					e.preventDefault();
					selected.togglePlay();
					break;
				case 'ArrowLeft':
					selected?.seek(-step);
					break;
				case 'ArrowRight':
					selected?.seek(step);
					break;
			}
		});
	}
</script>

<script lang="ts">
	import { PauseIcon, PlayIcon } from 'lucide-svelte';
	import * as Select from '$lib/components/ui/select';
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { browser } from '$app/environment';
	import { getVisualizationPlugin, type ControlRequirements, type VisualizationType } from '.';
	import { writable, type Writable } from 'svelte/store';
	import type { mode } from '$lib/analysis/modes';

	export let visualization: VisualizationType;
	export let computedData: mode.ComputedData<VisualizationType>;
	export let fileState: mode.FileState<VisualizationType>;

	let component = getVisualizationPlugin(visualization);
	let controls: ControlRequirements;
	let playing = false;
	let duration: number;
	let currentTime: number;
	let speed: { label?: string; value: number } = { value: 1 };
	let speedOptions: number[] = [];

	for (let i = 0.25; i <= 2.0; i += 0.25) {
		speedOptions.push(i);
	}

	function setAsSelected() {
		selected?.pause();

		$selectedStore = controls;
	}

	function speedChanger(newSelection: { label?: string; value: number } | undefined) {
		if (!newSelection) return;

		speed.value = newSelection.value;

		controls.setSpeed(speed.value);
	}

	function buttonPressEvent() {
		if (selected === controls) {
			selected.togglePlay();
		} else {
			setAsSelected();
			selected?.play();
		}
	}

	// TODO: implement a better method in time.ts
	function numberToTime(current: number): string {
		let time = new Date(current * 1000);

		return time.toLocaleString('en-GB', {
			minute: '2-digit',
			second: '2-digit',
			fractionalSecondDigits: 3
		});
	}
</script>

<section
	class="flex w-full flex-1 flex-col transition"
	class:opacity-80={$selectedStore !== controls}
>
	<div class="flex w-full flex-1 overflow-x-scroll">
		<Button
			class="h-full w-16 rounded-none rounded-l"
			variant="default"
			on:click={buttonPressEvent}
		>
			{#if playing}
				<PauseIcon />
			{:else}
				<PlayIcon />
			{/if}
		</Button>

		<div class="flex w-full flex-col">
			<svelte:component
				this={component}
				bind:controls
				{computedData}
				{fileState}
				bind:current={currentTime}
				bind:duration
				bind:playing
				{setAsSelected}
			/>

			<div
				class="flex h-8 flex-row items-center rounded-b bg-secondary bg-opacity-50 px-3 py-1 font-mono"
			>
				<div>
					{numberToTime(currentTime)}/{numberToTime(duration)}
				</div>

				<Separator orientation="vertical" class="mx-2" />

				<Select.Root selected={speed} onSelectedChange={speedChanger}>
					<Select.Trigger class="m-0 h-full w-fit bg-secondary text-secondary-foreground">
						{speed?.value.toFixed(2)}x
					</Select.Trigger>
					<Select.Content class="bg-secondary text-secondary-foreground">
						{#each speedOptions as speedItem}
							<Select.Item value={speedItem}>{speedItem.toFixed(2)}x</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>

				<div class="flex-1"></div>

				<Separator orientation="vertical" class="mx-2" />

				<div class="text-muted-foreground">
					{fileState.name}
				</div>
			</div>
		</div>
	</div>
</section>
