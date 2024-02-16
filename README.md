# Test environment
- Apple M2 Pro
- macOS 14.3

# Abstract
`download_models/app/multilingual-e5-large-onnx.zip` is a zipped file of the following link (MIT License):

https://huggingface.co/intfloat/multilingual-e5-large/tree/main/onnx

`docker-compose.yml` is based on the following link:

https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/#sample-docker-composeyml


# How to test
run `docker compose up -d --build`

```
$ curl -X PUT -H "Content-Type: application/json" -d @cluster_settings_options.json http://localhost:9200/_cluster/settings

{"acknowledged":true,"persistent":{"plugins":{"ml_commons":{"only_run_on_ml_node":"false","model_access_control_enabled":"true","native_memory_threshold":"99","allow_registering_model_via_url":"true"}}},"transient":{}}
```
```
$ curl -X POST -H "Content-Type: application/json" -d '{"name": "test-group"}' http://localhost:9200/_plugins/_ml/model_groups/_register

{"model_group_id":"GAk8sI0BqdUFht1E9zFe","status":"CREATED"}
```

Fix `model_group_id` in `models_register_options.json` as the response.

```
$ curl -X POST -H "Content-Type: application/json" -d @models_register_options.json http://localhost:9200/_plugins/_ml/models/_register

{"task_id":"HAldsI0BqdUFht1EfTH9","status":"CREATED"}
```
Use `task_id` in the response.
```
$ curl http://localhost:9200/_plugins/_ml/tasks/${task_id}

{"model_id":"HQldsI0BqdUFht1EfjE8","task_type":"REGISTER_MODEL","function_name":"TEXT_EMBEDDING","state":"COMPLETED","worker_node":["VspuhiSnS-mUMcXpIOEZZQ"],"create_time":1708060933626,"last_update_time":1708060933795,"is_async":true}
```
Use `model_id` in the response.
```
$ curl -X POST http://localhost:9200/_plugins/_ml/models/${model_id}/_deploy

{"task_id":"HglesI0BqdUFht1E6zGj","task_type":"DEPLOY_MODEL","status":"CREATED"}
```

The deployment completes with an error condition. The following is the log of `opensearch-node1` container:

```
2024-02-16 14:23:49 [2024-02-16T05:23:49,413][ERROR][o.o.m.e.a.DLModel        ] [opensearch-node1] Failed to deploy model HQldsI0BqdUFht1EfjE8
2024-02-16 14:23:49 java.lang.UnsatisfiedLinkError: no onnxruntime in java.library.path: :/usr/share/opensearch/plugins/opensearch-knn/lib:/usr/java/packages/lib:/usr/lib64:/lib64:/lib:/usr/lib
2024-02-16 14:23:49     at java.lang.ClassLoader.loadLibrary(ClassLoader.java:2434) ~[?:?]
2024-02-16 14:23:49     at java.lang.Runtime.loadLibrary0(Runtime.java:818) ~[?:?]
2024-02-16 14:23:49     at java.lang.System.loadLibrary(System.java:1989) ~[?:?]
2024-02-16 14:23:49     at ai.onnxruntime.OnnxRuntime.load(OnnxRuntime.java:338) ~[onnxruntime_gpu-1.14.0.jar:1.14.0]
2024-02-16 14:23:49     at ai.onnxruntime.OnnxRuntime.init(OnnxRuntime.java:139) ~[onnxruntime_gpu-1.14.0.jar:1.14.0]
2024-02-16 14:23:49     at ai.onnxruntime.OrtEnvironment$ThreadingOptions.<clinit>(OrtEnvironment.java:353) ~[onnxruntime_gpu-1.14.0.jar:1.14.0]
2024-02-16 14:23:49     at ai.djl.onnxruntime.engine.OrtEngine.<init>(OrtEngine.java:44) ~[onnxruntime-engine-0.21.0.jar:?]
2024-02-16 14:23:49     at ai.djl.onnxruntime.engine.OrtEngine.newInstance(OrtEngine.java:64) ~[onnxruntime-engine-0.21.0.jar:?]
2024-02-16 14:23:49     at ai.djl.onnxruntime.engine.OrtEngineProvider.getEngine(OrtEngineProvider.java:40) ~[onnxruntime-engine-0.21.0.jar:?]
2024-02-16 14:23:49     at ai.djl.engine.Engine.getEngine(Engine.java:187) ~[api-0.21.0.jar:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.doLoadModel(DLModel.java:185) ~[opensearch-ml-algorithms-2.11.1.0.jar:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.lambda$loadModel$1(DLModel.java:275) [opensearch-ml-algorithms-2.11.1.0.jar:?]
2024-02-16 14:23:49     at java.security.AccessController.doPrivileged(AccessController.java:569) [?:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.loadModel(DLModel.java:242) [opensearch-ml-algorithms-2.11.1.0.jar:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.initModel(DLModel.java:138) [opensearch-ml-algorithms-2.11.1.0.jar:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.MLEngine.deploy(MLEngine.java:125) [opensearch-ml-algorithms-2.11.1.0.jar:?]
2024-02-16 14:23:49     at org.opensearch.ml.model.MLModelManager.lambda$deployModel$52(MLModelManager.java:1003) [opensearch-ml-2.11.1.0.jar:2.11.1.0]
2024-02-16 14:23:49     at org.opensearch.core.action.ActionListener$1.onResponse(ActionListener.java:82) [opensearch-core-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.ml.model.MLModelManager.lambda$retrieveModelChunks$58(MLModelManager.java:1123) [opensearch-ml-2.11.1.0.jar:2.11.1.0]
2024-02-16 14:23:49     at org.opensearch.core.action.ActionListener$1.onResponse(ActionListener.java:82) [opensearch-core-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.action.support.ThreadedActionListener$1.doRun(ThreadedActionListener.java:78) [opensearch-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.common.util.concurrent.ThreadContext$ContextPreservingAbstractRunnable.doRun(ThreadContext.java:908) [opensearch-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.common.util.concurrent.AbstractRunnable.run(AbstractRunnable.java:52) [opensearch-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136) [?:?]
2024-02-16 14:23:49     at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635) [?:?]
2024-02-16 14:23:49     at java.lang.Thread.run(Thread.java:833) [?:?]
2024-02-16 14:23:49 [2024-02-16T05:23:49,439][ERROR][o.o.m.m.MLModelManager   ] [opensearch-node1] Failed to retrieve model HQldsI0BqdUFht1EfjE8
2024-02-16 14:23:49 org.opensearch.ml.common.exception.MLException: Failed to deploy model HQldsI0BqdUFht1EfjE8
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.lambda$loadModel$1(DLModel.java:289) ~[?:?]
2024-02-16 14:23:49     at java.security.AccessController.doPrivileged(AccessController.java:569) ~[?:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.loadModel(DLModel.java:242) ~[?:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.initModel(DLModel.java:138) ~[?:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.MLEngine.deploy(MLEngine.java:125) ~[?:?]
2024-02-16 14:23:49     at org.opensearch.ml.model.MLModelManager.lambda$deployModel$52(MLModelManager.java:1003) ~[?:?]
2024-02-16 14:23:49     at org.opensearch.core.action.ActionListener$1.onResponse(ActionListener.java:82) [opensearch-core-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.ml.model.MLModelManager.lambda$retrieveModelChunks$58(MLModelManager.java:1123) [opensearch-ml-2.11.1.0.jar:2.11.1.0]
2024-02-16 14:23:49     at org.opensearch.core.action.ActionListener$1.onResponse(ActionListener.java:82) [opensearch-core-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.action.support.ThreadedActionListener$1.doRun(ThreadedActionListener.java:78) [opensearch-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.common.util.concurrent.ThreadContext$ContextPreservingAbstractRunnable.doRun(ThreadContext.java:908) [opensearch-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at org.opensearch.common.util.concurrent.AbstractRunnable.run(AbstractRunnable.java:52) [opensearch-2.11.1.jar:2.11.1]
2024-02-16 14:23:49     at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136) [?:?]
2024-02-16 14:23:49     at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635) [?:?]
2024-02-16 14:23:49     at java.lang.Thread.run(Thread.java:833) [?:?]
2024-02-16 14:23:49 Caused by: java.lang.UnsatisfiedLinkError: no onnxruntime in java.library.path: :/usr/share/opensearch/plugins/opensearch-knn/lib:/usr/java/packages/lib:/usr/lib64:/lib64:/lib:/usr/lib
2024-02-16 14:23:49     at java.lang.ClassLoader.loadLibrary(ClassLoader.java:2434) ~[?:?]
2024-02-16 14:23:49     at java.lang.Runtime.loadLibrary0(Runtime.java:818) ~[?:?]
2024-02-16 14:23:49     at java.lang.System.loadLibrary(System.java:1989) ~[?:?]
2024-02-16 14:23:49     at ai.onnxruntime.OnnxRuntime.load(OnnxRuntime.java:338) ~[?:?]
2024-02-16 14:23:49     at ai.onnxruntime.OnnxRuntime.init(OnnxRuntime.java:139) ~[?:?]
2024-02-16 14:23:49     at ai.onnxruntime.OrtEnvironment$ThreadingOptions.<clinit>(OrtEnvironment.java:353) ~[?:?]
2024-02-16 14:23:49     at ai.djl.onnxruntime.engine.OrtEngine.<init>(OrtEngine.java:44) ~[?:?]
2024-02-16 14:23:49     at ai.djl.onnxruntime.engine.OrtEngine.newInstance(OrtEngine.java:64) ~[?:?]
2024-02-16 14:23:49     at ai.djl.onnxruntime.engine.OrtEngineProvider.getEngine(OrtEngineProvider.java:40) ~[?:?]
2024-02-16 14:23:49     at ai.djl.engine.Engine.getEngine(Engine.java:187) ~[?:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.doLoadModel(DLModel.java:185) ~[?:?]
2024-02-16 14:23:49     at org.opensearch.ml.engine.algorithms.DLModel.lambda$loadModel$1(DLModel.java:275) ~[?:?]
2024-02-16 14:23:49     ... 14 more
2024-02-16 14:23:49 [2024-02-16T05:23:49,442][INFO ][o.o.m.a.d.TransportDeployModelOnNodeAction] [opensearch-node1] deploy model task done HglesI0BqdUFht1E6zGj
2024-02-16 14:23:49 [2024-02-16T05:23:49,447][ERROR][o.o.m.a.f.TransportForwardAction] [opensearch-node1] deploy model failed on all nodes, model id: HQldsI0BqdUFht1EfjE8
2024-02-16 14:23:49 [2024-02-16T05:23:49,447][INFO ][o.o.m.a.f.TransportForwardAction] [opensearch-node1] deploy model done with state: DEPLOY_FAILED, model id: HQldsI0BqdUFht1EfjE8
```
