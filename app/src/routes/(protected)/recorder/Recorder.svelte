<script lang="ts">
	import RecorderSingle from './RecorderSingle.svelte';
	import * as Resizable from '$lib/components/ui/resizable';
	import * as Select from '$lib/components/ui/select';
	import type { PromptResponse } from './recorder';
	import { Button } from '$lib/components/ui/button';
	import JSZip from 'jszip';
	import { toast } from 'svelte-sonner';
	import { Toaster } from '$lib/components/ui/sonner';
	import type { Selected } from 'bits-ui';
	import Separator from '$lib/components/ui/separator/separator.svelte';

	export let prompts: PromptResponse[];
	export let promptName: string;
	export let recording = false;

	let selectedIndex: number = 0;
	let disableExport: boolean = false;
	let disableImport: boolean = false;

	let shortcutsEnabled: boolean = true;

	let selectedCamera: Selected<MediaDeviceInfo | null> = {
		label: 'Default camera',
		value: null
	};

	let selectedMic: Selected<MediaDeviceInfo | null> = {
		label: 'Default microphone',
		value: null
	};

	function prependZeros(desiredLength: number, currentString: string) {
		return '0'.repeat(desiredLength - currentString.length) + currentString;
	}

	async function downloadAllRecordings() {
		disableExport = true;
		const zip = new JSZip();
		let notes = '';
		for (let prompt of prompts) {
			let promptIndexPadded = prependZeros(4, '' + (prompt.index + 1));
			let promptName = promptIndexPadded + '-' + prompt.id;
			zip.file(`${promptName}.txt`, prompt.content);
			for (let i = 0; i < prompt.recordings.length; i++) {
				let recordingName =
					promptIndexPadded + '-' + prependZeros(3, '' + (i + 1)) + '-' + prompt.id;
				notes += recordingName + ': ' + prompt.recordings[i].note;
				zip.file(`${recordingName}.webm`, prompt.recordings[i].blob);
			}
		}
		zip.file('notes.txt', notes);
		zip
			.generateAsync({ type: 'blob' })
			.then(function (content: Blob) {
				const url = URL.createObjectURL(content);
				const a = document.createElement('a');
				a.href = url;
				a.download = `${promptName}.zip`;
				a.click();
				URL.revokeObjectURL(url);
			})
			.then(() => {
				disableExport = false;
			});
	}

	function importSession() {
		disableImport = true;
		const formData = new FormData();
		let data = [];
		for (let prompt of prompts) {
			let promptIndexPadded = prependZeros(4, '' + (prompt.index + 1));
			for (let i = 0; i < prompt.recordings.length; i++) {
				let recordingName =
					promptIndexPadded + '-' + prependZeros(3, '' + (i + 1)) + '-' + prompt.id;
				data.push({
					name: recordingName,
					groundTruth: prompt.content,
					note: prompt.recordings[i].note
				});
				formData.append(recordingName, prompt.recordings[i].blob);
			}
		}
		formData.append('data', JSON.stringify(data));
		formData.append('sessionName', promptName);
		fetch('?/importAudio', {
			method: 'POST',
			body: formData
		}).then(async (response) => {
			if (response.status == 200) {
				let data = JSON.parse((await response.json()).data);
				toast.success('Session ' + data[0] + ' has been created.', {
					description: 'Go to the session',
					action: {
						label: 'Session',
						onClick: () => {
							window.location.href = '/session/' + data[0];
						}
					}
				});
			}
			disableImport = false;
		});
	}

	function handleKeydown(event: KeyboardEvent) {
		if (!shortcutsEnabled) return;
		if (event.key === 'ArrowRight') {
			next();
		} else if (event.key === 'ArrowLeft') {
			previous();
		}
	}

	let videoDevices: MediaDeviceInfo[] | null = null;
	let audioDevices: MediaDeviceInfo[] | null = null;

	export async function getConnectedDevices(type: 'audioinput' | 'audiooutput' | 'videoinput') {
		const devices = await navigator.mediaDevices.enumerateDevices();
		return devices.filter((device) => device.kind === type);
	}

	const next = () =>
		!recording && (selectedIndex = Math.min(prompts.length - 1, selectedIndex + 1));
	const previous = () => !recording && (selectedIndex = Math.max(0, selectedIndex - 1));

	const windowSize = 2;
	$: center = Math.min(Math.max(windowSize, selectedIndex), prompts.length - windowSize);

	async function getAndLoadConnectedDevices(clear: boolean) {
		const videoDevicesAttempt = await getConnectedDevices('videoinput');
		const audioDevicesAttempt = await getConnectedDevices('audioinput');

		if (
			videoDevicesAttempt.filter((device) => device.deviceId !== '').length > 0 &&
			audioDevicesAttempt.filter((device) => device.deviceId !== '').length > 0
		) {
			videoDevices = videoDevicesAttempt;
			audioDevices = audioDevicesAttempt;
			selectedCamera.label = videoDevices[0].label;
			selectedMic.label = audioDevices[0].label;

			if (clear) {
				clearInterval(checkDeviceInterval);
			}
		}
	}

	const checkDeviceInterval = setInterval(() => getAndLoadConnectedDevices(true), 500);

	navigator.mediaDevices.addEventListener('devicechange', () => getAndLoadConnectedDevices(false));
</script>

<svelte:window on:keydown={handleKeydown} />

<main class="h-full">
	<Resizable.PaneGroup class="flex h-full" direction="horizontal">
		<Resizable.Pane
			class="z-30 flex flex-col gap-2 bg-secondary/50 p-4 pt-2 text-secondary-foreground"
			defaultSize={20}
		>
			<p class="text-muted-foreground">For session &lt;session-id&gt</p>

			<p>
				You have recorded {prompts.filter((prompt) => prompt.recordings.length > 0)
					.length}/{prompts.length} prompts
			</p>

			<div class="flex-1"></div>

			<Select.Root bind:selected={selectedCamera}>
				<Select.Trigger class="h-fit opacity-80 transition hover:opacity-100">
					{selectedCamera.label}
				</Select.Trigger>
				{#if videoDevices !== null}
					<Select.Content>
						{#each videoDevices as device}
							<Select.Item value={device}>{device.label}</Select.Item>
						{/each}
					</Select.Content>
				{/if}
			</Select.Root>

			<Select.Root bind:selected={selectedMic}>
				<Select.Trigger class="h-fit opacity-80 transition hover:opacity-100">
					{selectedMic.label}
				</Select.Trigger>
				{#if audioDevices !== null}
					<Select.Content>
						{#each audioDevices as device}
							<Select.Item value={device}>{device.label}</Select.Item>
						{/each}
					</Select.Content>
				{/if}
			</Select.Root>

			<Separator />

			<Button disabled={disableImport} on:click={importSession}>Export recording to session</Button>
			<Button disabled={disableExport} on:click={downloadAllRecordings} variant="outline"
				>Save files to disk</Button
			>
		</Resizable.Pane>

		<Resizable.Handle withHandle></Resizable.Handle>

		<Resizable.Pane class="relative mx-auto h-full py-4">
			{#each prompts
				.map((prompt, i) => ({ prompt, i }))
				.slice(center - windowSize, center + windowSize + 1) as { prompt, i } (prompt.id)}
				<section
					class:unselected={i !== selectedIndex}
					style:--index={i}
					style:--selected-index={selectedIndex}
					class="absolute z-20 h-[calc(100%-theme(space.8))] w-full overflow-y-scroll text-balance rounded p-4 text-center text-secondary-foreground transition"
				>
					<RecorderSingle
						bind:prompt={prompts[i]}
						bind:recording
						focused={i === selectedIndex}
						cameraInfo={selectedCamera.value}
						micInfo={selectedMic.value}
						onNext={next}
						onPrevious={previous}
						{shortcutsEnabled}
						enableShortcuts={() => {
							shortcutsEnabled = true;
						}}
						disableShortcuts={() => {
							shortcutsEnabled = false;
						}}
					/>
				</section>
			{/each}
		</Resizable.Pane>
	</Resizable.PaneGroup>
	<Toaster />
</main>

<style lang="postcss">
	section {
		--gap: calc(theme(maxWidth.xl) + theme(space.8));
		transform: translateX(calc((var(--index) - var(--selected-index)) * var(--gap))) var(--scale);

		transition-timing-function: cubic-bezier(0.2, 1, 0.22, 1);
		transition-duration: 1.2s;
	}

	.unselected {
		--scale: scale(0.95);
		@apply pointer-events-none z-0 opacity-50;
	}
</style>
