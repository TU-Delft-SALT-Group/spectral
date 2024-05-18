<script lang="ts" context="module">
	let selectedWavesurfer: Writable<WaveSurfer | null> = writable(null);
	let selectedRegion: Writable<RegionsPlugin | null> = writable(null);

	let selectedRegionValue: RegionsPlugin | null = null;
	let selectedWavesurferValue: WaveSurfer | null = null;

	const step = 0.5;

	selectedRegion.subscribe((value) => {
		selectedRegionValue = value;
	});
	selectedWavesurfer.subscribe((value) => {
		selectedWavesurferValue = value;
	});

	if (browser) {
		window.addEventListener('keydown', (e: KeyboardEvent) => {
			switch (e.key) {
				case 'ArrowRight':
					if (selectedWavesurferValue === null) return;

					selectedWavesurferValue.skip(step);

					break;
				case 'ArrowLeft':
					if (selectedWavesurferValue === null) return;

					selectedWavesurferValue.skip(-step);

					break;
				case 'Escape':
					if (selectedWavesurferValue === null) return;

					if (selectedRegionValue?.getRegions().length !== 0) {
						selectedRegionValue?.clearRegions();
					} else {
						selectedWavesurfer.set(null);
						selectedRegion.set(null);
					}
					break;
				case ' ':
					e.preventDefault();
					selectedWavesurferValue?.playPause();
					break;
			}
		});
	}
</script>

<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import type { SpecificModeData } from '..';
	import WaveSurfer from 'wavesurfer.js';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.esm.js';
	import { Button } from '$lib/components/ui/button';
	import { PauseIcon, PlayIcon } from 'lucide-svelte';
	import * as Select from '$lib/components/ui/select';
	import { Separator } from '$lib/components/ui/separator';
	import { writable, type Writable } from 'svelte/store';
	import { browser } from '$app/environment';

	export let item: SpecificModeData<'waveform'>;

	let wavesurfer: WaveSurfer;
	let currentTime = 0;
	let duration = 0;
	let regions: RegionsPlugin;
	let playing = false;
	let speed: { label?: string; value: number } = { value: 1 };
	let speedOptions: number[] = [];

	for (let i = 0.25; i <= 2.0; i += 0.25) {
		speedOptions.push(i);
	}

	onMount(() => {
		wavesurfer = new WaveSurfer({
			container: `#${item.fileId}-waveform`,
			url: `/db/${item.fileId}`,
			height: 'auto'
		});

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());

		wavesurfer.on('decode', () => {
			duration = wavesurfer.getDuration();
		});

		regions.enableDragSelection(
			{
				color: 'rgba(255, 0, 0, 0.1)'
			},
			10
		);

		regions.on('region-created', (region: Region) => {
			regions.getRegions().forEach((r) => {
				if (r.id === region.id) return;
				r.remove();
			});

			setAsSelected();
		});

		wavesurfer.on('timeupdate', (time: number) => {
			currentTime = time;
		});

		wavesurfer.on('interaction', () => {
			setAsSelected();
		});

		wavesurfer.on('play', () => {
			playing = true;
		});

		wavesurfer.on('pause', () => {
			playing = false;
		});
	});

	onDestroy(() => {
		regions.destroy();

		wavesurfer.destroy();
	});

	function setAsSelected() {
		$selectedWavesurfer?.pause();

		$selectedWavesurfer = wavesurfer;
		$selectedRegion = regions;
	}

	// TODO: implement a better method manually
	function numberToTime(current: number): string {
		let time = new Date(current * 1000);

		return time.toLocaleString('en-GB', {
			minute: '2-digit',
			second: '2-digit',
			fractionalSecondDigits: 3
		});
	}

	function speedChanger(newSelection: { label?: string; value: number } | undefined) {
		if (!newSelection) return;

		speed.value = newSelection.value;

		wavesurfer.setPlaybackRate(speed.value);
	}
</script>

<section
	class="flex w-full flex-1 flex-col transition"
	class:opacity-80={$selectedWavesurfer !== wavesurfer}
>
	<div class="flex w-full flex-1">
		<Button
			class="h-full w-16 rounded-none rounded-l"
			variant="default"
			on:click={() => {
				setAsSelected();
				wavesurfer.playPause();
			}}
		>
			{#if playing}
				<PauseIcon />
			{:else}
				<PlayIcon />
			{/if}
		</Button>

		<div class="flex w-full flex-col">
			<div
				id={`${item.fileId}-waveform`}
				class="waveform flex-1 overflow-x-scroll rounded-tr bg-secondary"
				role="region"
			></div>

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
					{item.name}
				</div>
			</div>
		</div>
	</div>
</section>
