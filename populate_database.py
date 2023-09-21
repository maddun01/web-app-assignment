## Quickstart script for fully populating the database

from web_application import app, db
from web_application.models.model import *
from web_application.utils import populate_tables
import datetime

with app.app_context():
    # Populate "hidden databases"
    # There are functions for these as they can be called when the application is running
    populate_tables(["1", "2"])
    print("Populated Datatypes and IPs")

    date = datetime.datetime.now()

    # Dictionaries used to assign the correct foreign keys to devices and networks
    ip_dict = {}
    datatype_dict = {}

    # Get the Ips and Datatypes from the tables
    ips = Ip.query.all()
    for ip in ips:
        ip_dict.update({ip.name: ip.id})
    datatypes = Datatype.query.all()
    for datatype in datatypes:
        datatype_dict.update({datatype.name: datatype.id})

    # Create and add Devices
    galaxy_a = Device(
        "Galaxy A32",
        "galaxya32",
        "Android R",
        ip_dict["A55"],
        date,
        None,
    )
    galaxy_s = Device(
        "Galaxy S23", "galaxys23", "Android O", ip_dict["G57"], date, None
    )
    galaxy_z = Device(
        "Galaxy Z Flip5", "galaxyzflip", "Android Q", ip_dict["G77"], date, None
    )
    galaxy_a54 = Device(
        "Galaxy A54", "galaxya54", "Android X", ip_dict["X2"], date, None
    )
    redmi_k50 = Device(
        "Redmik 50 Pro",
        "redmik50",
        "Android S",
        ip_dict["X2"],
        date,
        None,
    )
    redmi_k60 = Device(
        "Redmik 60 Ultra",
        "redmik60",
        "Android K",
        ip_dict["X2"],
        date,
        None,
    )
    pixel_8 = Device(
        "Pixel 8 Pro",
        "pixel8pro",
        "Android P",
        ip_dict["A76"],
        date,
        None,
    )
    pixel_7 = Device(
        "Pixel 7",
        "pixel7",
        "Android B",
        ip_dict["A76"],
        date,
        None,
    )
    mate_x3 = Device(
        "Mate X3",
        "huaweimatex3",
        "Android H",
        ip_dict["X1"],
        date,
        None,
    )
    mate_xs2 = Device(
        "Mate Xs 2",
        "huaweimatexs2",
        "Android J",
        ip_dict["X2"],
        date,
        None,
    )

    db.session.add_all(
        [
            galaxy_a,
            galaxy_s,
            galaxy_z,
            galaxy_a54,
            redmi_k50,
            redmi_k60,
            pixel_8,
            pixel_7,
            mate_x3,
            mate_xs2,
        ]
    )
    db.session.commit()
    print("Populated Devices")

    # Create and add Networks
    mobilenet = Network(
        "MobileNet v2",
        datatype_dict["f16"],
        "https://gitlab-zoo.ml.arm.com/mobilenet_v2",
        "mobilenet",
        date,
        date,
    )
    yolo = Network(
        "Yolo v4",
        datatype_dict["uint8"],
        "https://gitlab-zoo.ml.arm.com/yolo_v4_tiny_quant",
        "tiny_quant",
        date,
        None,
    )
    ai_bench = Network(
        "AI Benchmark Inception v3",
        datatype_dict["uint8"],
        "https://gitlab-zoo.ml.arm.com/ai_benchmark_inception_v3",
        "inception",
        date,
        None,
    )
    efficientnet_b6 = Network(
        "EfficientNet B6",
        datatype_dict["f32"],
        "https://gitlab-zoo.ml.arm.com/efficientnet_b6",
        "efficientnet",
        date,
        None,
    )
    micro_vision = Network(
        "Micro Vision",
        datatype_dict["int8"],
        "https://gitlab-zoo.ml.arm.com/micro_vision",
        "microvision",
        date,
        None,
    )
    resnet_v2 = Network(
        "ResNet v2 50",
        datatype_dict["int8"],
        "https://gitlab-zoo.ml.arm.com/resnet_v2_50",
        "resnetv250",
        date,
        None,
    )
    vgg_19 = Network(
        "VGG 19",
        datatype_dict["f32"],
        "https://gitlab-zoo.ml.arm.com/vgg19",
        "vgg19",
        date,
        None,
    )
    bytenet = Network(
        "ByteNet",
        datatype_dict["f16"],
        "https://gitlab-zoo.ml.arm.com/bytenet",
        "bytenet",
        date,
        None,
    )
    tinywav = Network(
        "Tiny Wav2Letter",
        datatype_dict["int8"],
        "https://gitlab-zoo.ml.arm.com/tiny_wav2letter",
        "tinywav2letter",
        date,
        None,
    )
    rnnoise = Network(
        "RNNoise",
        datatype_dict["f16"],
        "https://gitlab-zoo.ml.arm.com/rnnoise",
        "rnnoise",
        date,
        None,
    )

    db.session.add_all(
        [
            mobilenet,
            yolo,
            ai_bench,
            efficientnet_b6,
            micro_vision,
            resnet_v2,
            vgg_19,
            bytenet,
            tinywav,
            rnnoise,
        ]
    )
    db.session.commit()
    print("Populated Networks")

    # Create and add Users
    admin_user = User("admin@admin.com", "admin", "admin")
    general_user = User("user@user.com", "user", "user")
    db.session.add_all([admin_user, general_user])
    db.session.commit()

    # Get the admin account from the table
    admin_id = User.query.filter_by(email="admin@admin.com").first()
    admin = db.session.get(User, admin_id.id)

    # Assign admin privileges
    admin.is_admin = True
    db.session.add(admin)
    db.session.commit()
    print("Populated Users")
    print("Done")
