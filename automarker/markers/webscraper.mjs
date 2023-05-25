import { Marker, Step } from "./utils.mjs";
import SavePage from "../actions/webscraper/save-page.mjs";
import CopyOurPytests from "../actions/python/copy-our-tests.mjs";
import RunPytests from "../actions/python/run-pytests.mjs";
import CreateVirtualEnv from "../actions/python/create-virtual-env.mjs";
import DoInstallPytest from "../actions/python/do-install-pytest.mjs";
import DoRequirementsInstall from "../actions/python/do-requirements-install.mjs";

export class WebScraper extends Marker {
  steps = [
    new Step({ Action: SavePage }),
    new Step({ Action: CreateVirtualEnv }),
    new Step({ Action: DoInstallPytest }),
    new Step({ Action: DoRequirementsInstall, actionArgs: { useOurs: true } }),
    new Step({ Action: CopyOurPytests }),
    new Step({ Action: RunPytests, name: "running our tests" }),
  ];
}
