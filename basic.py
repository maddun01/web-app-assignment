from app import *
import datetime

with app.app_context():
    # for i in range(1, 3):
    #     delete = db.session.get(Device, i)
    #     db.session.delete(delete)

    # for i in range(1, 3):
    #     delete = db.session.get(Network, i)
    #     db.session.delete(delete)

    # for i in range(1, 5):
    #     delete = db.session.get(Datatype, i)
    #     db.session.delete(delete)

    # db.session.commit()
    # # breakpoint()
    date = datetime.datetime.now()

    galaxy = Device(
        "galaxya32-5g-remote-RFCR20WQJMA", "galaxy", "Android R", date, date
    )
    redmik50 = Device(
        "redmik50-pro-adb-wifi-IJK7ZPVCC6594LGE", "redmik50", "Android S", date, date
    )

    mobilenet = Network(
        "MobileNet v1",
        "https://gitlab-zoo.ml.arm.com/ML/arm-model-zoo/-/tree/master/models/image_classification/mobilenet_v2_1.0_224",
        "TFLite",
        date,
        date,
    )

    yolo = Network(
        "Yolo v4",
        "https://gitlab-zoo.ml.arm.com/ML/arm-model-zoo/-/tree/master/models/Benchmarks/ai_benchmark/v5/yolo_v4_tiny_quant/tflite_uint8",
        "TFLite",
        date,
        date,
    )

    db.session.add_all([galaxy, redmik50, mobilenet, yolo])
    db.session.commit()

    f16 = Datatype("f16", mobilenet.id)
    f32 = Datatype("f32", mobilenet.id)
    int8 = Datatype("int8", redmik50.id)
    uint8 = Datatype("uint8", redmik50.id)
    db.session.add_all([f16, f32, int8, uint8])
    db.session.commit()

    print(Device.query.all())
    print("\n")
    # print (db.session.get(Network, 1))
    # print(Network.query.all())
    for network in Network.query.all():
        print(network)
        print(network.display_datatypes())
        print("")
