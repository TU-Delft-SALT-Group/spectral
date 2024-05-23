<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { Button } from '$lib/components/ui/button';
	import { MicIcon } from 'lucide-svelte';
	import type { Action } from 'svelte/action';
	import WaveSurfer from 'wavesurfer.js';
	import RecordPlugin from 'wavesurfer.js/dist/plugins/record.esm.js';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import { Input } from '$lib/components/ui/input';
	import { string } from 'zod';

	export let sessionId: string;

	let wavesurfer: WaveSurfer | null = null;
	let recorder: RecordPlugin | null = null;

	let recordButton: HTMLDivElement;

	let recording = false;

	const mountWavesurferRecording: Action = (node) => {
		wavesurfer = WaveSurfer.create({
			container: node,
			waveColor: window.getComputedStyle(recordButton).color,
			progressColor: window.getComputedStyle(recordButton).color,
			duration: 22
		});

		recorder = wavesurfer.registerPlugin(
			RecordPlugin.create({ scrollingWaveform: true, renderRecordedAudio: false })
		);

		wavesurfer.on('finish', () => {
			wavesurfer?.setTime(0);
		});

		recorder?.startRecording();
		recording = true;

		recorder?.on('record-end', async (blob: Blob) => (recordingBlob = blob));

		return {
			destroy() {
				wavesurfer?.destroy();
			}
		};
	};

	$: if (!recording) {
		if (recorder?.isRecording()) {
			recorder?.stopRecording();
			open = true;
		}
	}

	async function uploadRecording() {

		if (recordingBlob != null) {
			const formData = new FormData();

			formData.append('recording', recordingBlob);

			formData.append('groundTruth', groundTruth);

			await fetch(`${sessionId}/${filename}?`, {
				method: 'POST',
				body: formData
			});
		}

		filename = '';
		groundTruth = '';

		await invalidateAll();
	}

	let recordingBlob: Blob | null = null;
	let filename = '';
	let groundTruth = '';
	let open = false;
</script>

<AlertDialog.Root bind:open>
	<Button
		class="relative h-10 w-full bg-red-800 bg-opacity-80 p-0 text-white shadow hover:bg-red-700"
		on:click={() => {
			recording = !recording;
		}}
	>
		<MicIcon class="h-5 w-5 transition {recording && 'opacity-0'}"></MicIcon>
		<span class="pl-2 transition" class:opacity-0={recording}> Record </span>

		{#if recording}
			<!-- Height is 40/128 because apparently the min height of wavesurfer canvas is 128px but I want it to be 40px. If the button height is changed, change that 40 to whatever the new height is (in pixels) -->
			<div
				use:mountWavesurferRecording
				bind:this={recordButton}
				class="pointer-events-none absolute bottom-0 w-full scale-y-[calc(40/128)]"
			></div>
		{/if}
	</Button>

	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Enter name for recording</AlertDialog.Title>
			<AlertDialog.Description>
				<Input type="text" name="filename" minlength={1} required bind:value={filename}></Input>
			</AlertDialog.Description>
			<AlertDialog.Title>Enter the ground truth</AlertDialog.Title>
			<AlertDialog.Description>
				<Input type="text" name="groundTruth" bind:value={groundTruth}></Input>
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel on:click={() => (open = false)}>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action on:click={() => uploadRecording()}>Continue</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>

<svelte:window
	on:keydown={(e) => {
		if (e.code === 'KeyR' && e.shiftKey) {
			recording = !recording;
			return;
		}

		if (e.key === 'Enter' && open && filename.length > 0) {
			uploadRecording();
			open = false;
		}
	}}
/>

<style>
	div {
		transform-origin: bottom;
	}
</style>
