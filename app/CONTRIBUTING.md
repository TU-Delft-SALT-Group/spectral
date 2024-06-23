# Contributing to app

Make sure to take a look to the [general contributing guidelines](https://github.com/TU-Delft-SALT-Group/spectral/CONTRIBUTING.md).

There are two main aspects one might want to contribute to in this repo: adding a new mode or general contributing. Each one has different considerations, both of which are outlined below.

<!--toc:start-->

- [General contributing](#general-contributing)
  - [Framework](#framework)
  - [Package manager](#package-manager)
  - [Styling](#styling)
- [Adding a new mode](#adding-a-new-mode) - [Declaring mode data](#declaring-mode-data) - [Adding components](#adding-components) - [Registering the new mode](#registering-the-new-mode) - [Kernel side](#kernel-side)
<!--toc:end-->

## General contributing

### Framework

The framework used is SvelteKit. Svelte and SvelteKit are some of the quickest-to-learn frameworks out there. The best way to do is by following [the official tutorial](https://learn.svelte.dev).

### Package manager

We use pnpm. Install pnpm following [the instructions on the website](https://pnpm.io/installation).

Then install dependencies with

```bash
pnpm install # or `pnpm i`
```

Dependencies should be automatically installed with `docker compose up --build`. However, you should install dependencies for the IDE language server to pick up type definitions and such.

Other than that, `pnpm` is mostly used to add new dependencies (either `pnpm add <dep>` for production dependencies or `pnpm add -D <dep>` for development dependencies)

### Styling

We use [tailwind](https://tailwindcss.com) for styling and [shadcn-svelte](https://www.shadcn-svelte.com) for components.

Try to use tailwind for most styling. Of course, if you want to something more complicated you can use regular `<style>` tags.

You can browse the available shadcn components and usage at [the website](https://www.shadcn-svelte.com/docs). If a component is not in the project already, you can add it via:

```bash
pnpm dlx shadcn-svelte add <component>
```

### Testing

The frontend side is tested with end-to-end integration tests built with [Playwright](https://playwright.dev/) and unit tests made with [vitest](https://vitest.dev/).

#### Unit tests

Unit tests are distributed all arould the place, being stored near the files they are related to. For example, under `src/lib/files/size.test.ts` you can find tests related to correctly showing filesizes.

#### Integration tests

The more interesting, and, arguably more important part of our testing suite are playwright tests: these are end-to-end tests, that simulate different actions on the web-facing application, and then check that we can see what we can see on the screen. The errors with these tests can be related to errors anywhere else in the project: e.g. if nginx configuration is incorrect, these tests would fail. Hence you should view these tests as a largely false-negative one: if it fails, then it is not necessarily your problem, but it still needs attention. So, if these tests fail on the dev branch, you should contact somebody about it. We will include large proportion of these tests in the CI, so that if these tests are failing, the functionality won't be merged, however, these tests run for a very long time, so make sure to rerun these tests yourself to not strain our CI servers :)

The playwright tests should be added under `tests/` folder, and they can be run with `pnpm test:integration`. To install all the playwright dependencies, make sure to run `pnpm exec playwright install && pnpm exec playwright install-deps` in your terminal.

_Note: we currently run the tests only for Blink and Gecko, no webkit, since the support for webkit on various linuxes seems unstable_

## Adding a new mode

Adding new modes of analysis is designed to be as straghtforward as possible, while still being as flexible as possible.

As an overview, each modes needs to declare:

- A name
- Data it expects from the kernel
- File state
- Mode state
- A component that displays the data
- An icon

> If any step in the following instructions is unclear, you can always take a look to how other modes are implemented.

### Declaring mode data

First, create the file `app/src/lib/analysis/modes/<your-mode>/index.ts`. Here you declare the data following this template:

```typescript
import { z } from 'zod';
import type { ModeValidator } from '..';
import { fileState } from '../file-state';

export const yourModeData = {
	computedFileData: /* TODO */,

	fileState: fileState
		.pick({
			/* TODO */
		})
		.default({}),

	modeState: z.object({
		/* TODO */
	}).default({})
} satisfies ModeValidator;
```

Then you need to fill in each field. Each field is a [zod](https://zod.dev/) parser, which defines shapes that can be validated at runtime. Visit the [zod docs](https://zod.dev/?id=introduction) for more info.

- `computedFileData` is the data that is directly computed from the file. This info should be implemented in the Kernel.
- `modeState` is synced state that is stored per-mode (and per-pane). Used for things such as toggles and sliders set by the user. For example, whether to show the legend in the graph.
- `fileState` is state that is stored with each file, globally. For example, playback speed or selected frame. The file state is global for all modes. So, instead of declaring it in the mode data directly, it is declared in `file-state` and the mode picks fields from there. The file state is passed to the kernel as additional info (this is mainly used to send frames).

Both `modeState` and `fileState` need to provide a default (this is because the state needs to be somehow initialized at some point).

### Adding components

Create a new component in `your-mode/YourMode.svelte`:

```svelte
<script lang="ts">
	import type { ModeComponentProps } from '..';

	export let fileData: ModeComponentProps<'your-mode'>['fileData'];
	export let modeState: ModeComponentProps<'your-mode'>['modeState'];
</script>

<!-- Implement your component here -->
```

It is convenient to re-export the new mode from `.../modes/<your-mode>/index.ts`:

```ts
/** ... */

export { default as YourMode } from 'YourMode.svelte';
```

### Registering the new mode

Finally you have to register your new mode in `modes/index.ts`. You need to add the mode data in the `modes` constant:

```ts
export const modes = {
	'simple-info': simpleInfoData,
	waveform: waveformData,
	spectrogram: spectrogramData,
	'vowel-space': vowelSpaceData,
	transcription: transcriptionData,
	'your-mode': yourModeData
} as const satisfies Record<string, ModeValidator>;
```

Then register the component and the icon

```ts
export const modeComponents: {
	[M in keyof typeof modes]: {
		component: ModeComponent<M>;
		icon: ComponentType;
	};
} = {
	'simple-info': {
		component: SimpleInfo,
		icon: InfoIcon
	},

	waveform: {
		component: Waveform,
		icon: AudioWaveformIcon
	},

	spectrogram: {
		component: Spectrogram,
		icon: SpectrogramIcon
	},

	'vowel-space': {
		component: VowelSpace,
		icon: VowelSpaceIcon
	},

	transcription: {
		component: Transcription,
		icon: CaptionsIcon
	},

	'your-mode': {
		component: YourMode,
		icon: YourModeIcon
	}
};
```

The icon can be custom made, but you can also use one from [lucide](https://lucide.dev/) if appropriate.

### Kernel side

You need to implement and endpoint in the Python side with the same name as your mode that provides whatever you have declared that `computedData` should return.
