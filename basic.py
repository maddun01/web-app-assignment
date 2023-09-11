from web_application import app, db

# from web_application.models.datatype_model import Datatype
# from web_application.models.device_model import Device
# from web_application.models.ip_model import Ip
# from web_application.models.network_model import Network
from web_application.models.model import *
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

    # for i in range(1, 7):
    #     delete = db.session.get(Ip, i)
    #     db.session.delete(delete)

    # db.session.commit()
    # breakpoint()
    date = datetime.datetime.now()

    # # add datatypes
    # f16 = Datatype("f16")
    # f32 = Datatype("f32")
    # int8 = Datatype("int8")
    # uint8 = Datatype("uint8")
    # db.session.add_all([f16, f32, int8, uint8])
    # db.session.commit()

    # # add ips
    # a55 = Ip("A55")
    # a76 = Ip("A76")
    # g57 = Ip("G57")
    # g77 = Ip("G77")
    # x1 = Ip("X1")
    # x2 = Ip("X2")
    # db.session.add_all([a55, a76, g57, g77, x1, x2])
    # db.session.commit()

    # print("Added IPs and Datatypes ")
    # breakpoint()

    a55 = Ip.query.filter_by(name="A55").first()
    x2 = Ip.query.filter_by(name="X2").first()
    f16 = Datatype.query.filter_by(name="f16").first()
    f32 = Datatype.query.filter_by(name="f32").first()

    # add devices
    galaxy = Device(
        "galaxya32-5g-remote-RFCR20WQJMA", "galaxya32", "Android R", a55.id, date, date
    )
    redmik50 = Device(
        "redmik50-pro-adb-wifi-IJK7ZPVCC6594LGE",
        "redmik50",
        "Android S",
        x2.id,
        date,
        date,
    )

    # add networks
    mobilenet = Network(
        "MobileNet v1",
        f16.id,
        "https://gitlab-zoo.ml.arm.com/ML/arm-model-zoo/-/tree/master/models/image_classification/mobilenet_v2_1.0_224",
        "TFLite",
        date,
        date,
    )

    yolo = Network(
        "Yolo v4",
        f32.id,
        "https://gitlab-zoo.ml.arm.com/ML/arm-model-zoo/-/tree/master/models/Benchmarks/ai_benchmark/v5/yolo_v4_tiny_quant/tflite_uint8",
        "TFLite",
        date,
        date,
    )

    db.session.add_all([galaxy, redmik50, mobilenet, yolo])
    db.session.commit()

    print("Added devices and networks")

    # print(Device.query.all())
    # print("\n")
    # # print (db.session.get(Network, 1))
    # # print(Network.query.all())
    # for network in Network.query.all():
    #     print(network)
    #     print(network.display_datatypes())
    #     print("")
