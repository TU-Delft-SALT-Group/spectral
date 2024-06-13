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
	import PauseIcon from 'lucide-svelte/icons/pause';
	import PlayIcon from 'lucide-svelte/icons/play';
	import * as Select from '$lib/components/ui/select';
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { browser } from '$app/environment';
	import {
		getVisualizationPlugin,
		numberToTime,
		type ControlRequirements,
		type VisualizationType
	} from '.';
	import { writable, type Writable } from 'svelte/store';
	import type { mode } from '$lib/analysis/modes';

	export let visualization: VisualizationType;
	export let computedData: mode.ComputedData<VisualizationType>;
	export let fileState: mode.FileState<VisualizationType>;
	let width: number;

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
</script>

<section
	bind:clientWidth={width}
	class="flex h-fit flex-col transition"
	class:opacity-80={$selectedStore !== controls}
>
	<div class="flex h-fit w-full">
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

		<div class="flex h-fit w-full flex-col">
			<svelte:component
				this={component}
				bind:controls
				{computedData}
				{fileState}
				bind:current={currentTime}
				bind:duration
				bind:playing
				{setAsSelected}
				width={width - 48}
			/>

			<!-- the bar -->
			<div
				class="flex h-8 flex-row items-center overflow-x-hidden rounded-b bg-secondary bg-opacity-50 px-3 py-1 font-mono"
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

				<div class="ml-auto"></div>

				<Separator orientation="vertical" class="mx-2" />

				<div class="w-full text-ellipsis text-muted-foreground">
					{fileState.name}
				</div>
			</div>
			<!-- end of bar -->
		</div>
	</div>
</section>
