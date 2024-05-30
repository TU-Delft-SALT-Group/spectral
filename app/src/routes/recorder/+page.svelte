<script lang="ts">
	import JSZip from 'jszip';
	import webmToMp4 from 'webm-to-mp4';

	let mediaStream: MediaStream;
	let mediaRecorder: MediaRecorder;
	let recordedChunks: Blob[] = [];
	let videoURL: string = '';
	let isRecording: boolean = false;
	let recorded: boolean = false;
	let prompts: string[] | null = null;
	let promptIds: string[] | null = null;
	let recordings: (string | null)[] | null = null;
	let promptIndex = 0;
	let fileName: string = '';

	// Function to handle the file input change event
	function handleFileUpload(event: Event): void {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files.length > 0) {
			const file = input.files[0];
			fileName = file.name;
			if (file.type === 'text/plain') {
				const reader = new FileReader();
				reader.onload = () => {
					let fileContent = reader.result as string;
					promptIndex = 0;
					prompts = [];
					promptIds = [];
					recordings = [];
					console.log(fileContent);
					for (let line of fileContent.split(/\r?\n/)) {
						console.log(line);
						let indexSplit = line.indexOf(' ');
						promptIds.push(line.substring(0, indexSplit));
						prompts.push(line.substring(indexSplit));
						recordings.push(null);
					}
				};
				reader.readAsText(file);
			} else {
				alert('Please upload a valid .txt file.');
			}
		}
	}

	// Start the video and audio stream and recorder
	async function startRecording(): Promise<void> {
		try {
			mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
			const videoPreview = document.querySelector<HTMLVideoElement>('#video-preview');
			if (videoPreview) {
				videoPreview.srcObject = mediaStream;
				videoPreview.muted = true; // Mute the audio during recording
			}
			mediaRecorder = new MediaRecorder(mediaStream, { mimeType: 'video/webm' });

			mediaRecorder.ondataavailable = (event: BlobEvent) => {
				if (event.data.size > 0) {
					recordedChunks.push(event.data);
				}
			};

			mediaRecorder.onstop = () => {
				const blob = new Blob(recordedChunks, { type: 'video/webm' });
				videoURL = URL.createObjectURL(blob);
				if (recordings !== null) {
					recordings[promptIndex] = videoURL;
				}
				recordedChunks = [];
				recorded = true;
			};

			mediaRecorder.start();
			isRecording = true;
			recorded = false; // Reset the recorded state
		} catch (err) {
			console.error('Error accessing media devices.', err);
		}
	}

	// Stop the video and audio recording
	function stopRecording(): void {
		if (mediaRecorder && isRecording) {
			mediaRecorder.stop();
			mediaStream.getTracks().forEach((track) => track.stop());
			isRecording = false;
		}
	}

	// Restart recording by resetting recordedChunks and starting a new recording
	function restartRecording(): void {
		recordedChunks = [];
		videoURL = '';
		startRecording();
	}

	function increaseIndex(): void {
		promptIndex++;
	}

	function decreaseIndex(): void {
		promptIndex--;
	}

	async function downloadAllRecordings() {
		if (recordings !== null && promptIds !== null && prompts !== null) {
			const zip = new JSZip();
			for (let i = 0; i < recordings.length; i++) {
				const cur = recordings[i];
				if (cur !== null) {
					const response = await fetch(cur, {
						method: 'GET',
						mode: 'cors', // You might need to adjust the mode based on your server's configuration
						cache: 'no-cache',
						credentials: 'same-origin',
						headers: {
							'Content-Type': 'application/octet-stream'
						},
						redirect: 'follow',
						referrerPolicy: 'no-referrer'
					});
					const blob = new Blob([await webmToMp4(new Uint8Array(await response.arrayBuffer()))], {
						type: 'video/mp4'
					});
					zip.file(`${promptIds[i]}.mp4`, blob);
					zip.file(`${promptIds[i]}.txt`, prompts[i]);
				}
			}
			zip.generateAsync({ type: 'blob' }).then(function (content: Blob) {
				const url = URL.createObjectURL(content);
				const a = document.createElement('a');
				a.href = url;
				a.download = fileName + '.zip';
				a.click();
				URL.revokeObjectURL(url);
			});
		}
	}
</script>

<div class="h-full w-full rounded">
	<div class="flex h-full flex-col border-8">
		<div id="top-part" class="flex h-4/5 w-full bg-gray-100">
			<div class="flex h-full w-full items-center justify-center bg-gray-500">
				{#if recordings === null}
					<p class="text-6xl" class:hidden={recorded || isRecording}>First upload prompts</p>
				{:else}
					<p class="text-6xl" class:hidden={recordings[promptIndex] !== null || isRecording}>
						Start a recording
					</p>
					<!-- svelte-ignore a11y_media_has_caption -->
					<video class="m-4" id="video-preview" autoplay playsinline class:hidden={!isRecording}
					></video>
					<!-- svelte-ignore a11y_media_has_caption -->
					<video
						class="m-4"
						id="video-playback"
						src={recordings[promptIndex]}
						controls
						class:hidden={recordings[promptIndex] === null || isRecording}
					></video>
				{/if}
			</div>
			<div class="w-1/3">
				<div class="m-4 rounded bg-gray-200">
					{#if prompts === null}
						<p class="border-2 text-3xl text-red-600">Prompts still have to be uploaded</p>
					{:else}
						<p class="border-2 text-3xl">
							{prompts[promptIndex]}
						</p>
					{/if}
				</div>
			</div>
		</div>
		<div id="top-part" class="h-1/5">
			{#if isRecording}
				<button on:click={stopRecording}>Stop Recording</button>
			{:else if recordings !== null && recordings[promptIndex] === null}
				<button on:click={startRecording}>Start Recording</button>
			{:else}
				<button on:click={restartRecording}>Restart Recording</button>
			{/if}
			<button disabled={recordings === null || promptIndex === 0} on:click={decreaseIndex}>
				Previous
			</button>
			<button
				disabled={recordings === null || promptIndex === recordings.length - 1}
				on:click={increaseIndex}
			>
				Next
			</button>
			<div>
				<input type="file" accept=".txt" on:change={handleFileUpload} class="file-upload" />
			</div>
			{#if recordings !== null}
				<button on:click={downloadAllRecordings}>Download All Recordings</button>
			{/if}
		</div>
	</div>
</div>

<style>
	video {
		max-width: 100%;
		max-height: 100%;
	}
	button {
		margin-right: 5px;
	}
	.hidden {
		display: none;
	}
</style>
