import type {
	DockviewApi,
	DockviewPanelApi,
	GroupPanelPartInitParameters,
	IContentRenderer,
	IDockviewPanelHeaderProps,
	ITabRenderer,
	PanelUpdateEvent,
	Parameters
} from 'dockview-core';

import { mount, unmount, type ComponentType, type SvelteComponent } from 'svelte';
export { default as simple } from './simple.svelte';
export { default as tab } from './tab.svelte';

export type ComponentProps = {
	params: IDockviewPanelHeaderProps;
};

export function mountComponent<S extends ComponentType<SvelteComponent<ComponentProps>>>(
	component: S,
	props: ComponentProps,
	element: HTMLElement
) {
	let mounted = mount(component, {
		target: element,
		props
	});

	return {
		update: (newProps: ComponentProps) => {
			mounted = { ...mounted, ...newProps };
		},
		dispose: () => {
			unmount(mounted);
		}
	};
}

abstract class AbstractSvelteRenderer {
	readonly _element: HTMLElement;

	get element() {
		return this._element;
	}

	constructor() {
		this._element = document.createElement('section');
		this.element.className = 'dv-vue-part';
		this.element.style.height = '100%';
		this.element.style.width = '100%';
	}
}

export class SvelteRenderer<S extends ComponentType<SvelteComponent<ComponentProps>>>
	extends AbstractSvelteRenderer
	implements IContentRenderer, ITabRenderer
{
	readonly _component: S;
	private _renderDisposable:
		| { update: (props: ComponentProps) => void; dispose: () => void }
		| undefined;
	private _api: DockviewPanelApi | undefined;
	private _containerApi: DockviewApi | undefined;

	constructor(component: S) {
		super();
		this._component = component;
	}

	init(parameters: GroupPanelPartInitParameters): void {
		this._api = parameters.api;
		this._containerApi = parameters.containerApi;

		const panelHeaderProps: IDockviewPanelHeaderProps = {
			params: parameters.params,
			api: parameters.api,
			containerApi: parameters.containerApi
		};

		this._renderDisposable?.dispose();
		this._renderDisposable = mountComponent(
			this._component,
			{ params: panelHeaderProps },
			this._element
		);
	}

	update(event: PanelUpdateEvent<Parameters>): void {
		if (this._api === undefined || this._containerApi === undefined) {
			return;
		}

		const params = event.params;

		this._renderDisposable?.update({
			params: {
				params,
				api: this._api,
				containerApi: this._containerApi
			}
		});
	}

	dispose(): void {
		this._renderDisposable?.dispose();
	}
}
