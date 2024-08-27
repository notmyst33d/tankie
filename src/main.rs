use std::env;
use std::process::Command;
use std::ffi::CString;
use russimp_sys::*;

macro_rules! sp {
    ($s:expr) => { CString::new($s).unwrap().as_ptr() as *const i8 }
}

fn main() {
    let args = env::args().collect::<Vec<String>>();

    // Step 1: Convert 3DS to GLB
    unsafe {
        let scene = aiImportFile(sp!(args[1].clone()), aiPostProcessSteps_aiProcess_DropNormals);
        let objects = std::slice::from_raw_parts((*(*scene).mRootNode).mChildren, (*(*scene).mRootNode).mNumChildren as usize);

        // Individual models should never have more than
        // one object... but what if we allow more than one object?
        if objects.len() > 1 {
            println!("!!! ALERTA ALERTA ALERTA ALERTA ALERTA ALERTA !!!");
            println!("!!! ALERTA ALERTA ALERTA ALERTA ALERTA ALERTA !!!");
            println!("!!! ALERTA ALERTA ALERTA ALERTA ALERTA ALERTA !!!");
            println!("YOU ARE CONVERTING A MODEL WITH MORE THAN ONE ROOT OBJECT");
            println!("THIS WILL FUCK SHIT UP SO GOOD LUCK");
            println!("!!! ALERTA ALERTA ALERTA ALERTA ALERTA ALERTA !!!");
            println!("!!! ALERTA ALERTA ALERTA ALERTA ALERTA ALERTA !!!");
            println!("!!! ALERTA ALERTA ALERTA ALERTA ALERTA ALERTA !!!");
        }

        for i in 0..objects.len() {
            // By default the models will have their origin set in ebenya, so lets fix it
            let translation = aiVector3D { x: 0.0, y: 0.0, z: 0.0 };
            // Make scaling realistic
            let scaling = aiVector3D { x: 0.01, y: 0.01, z: 0.01 };
            aiMatrix4Translation(&mut (*objects[i]).mTransformation as *mut aiMatrix4x4, &translation);
            aiMatrix4Scaling(&mut (*objects[i]).mTransformation as *mut aiMatrix4x4, &scaling);
        }

        aiExportScene(scene, sp!("glb2"), sp!(args[1].clone().replace(".3ds", ".glb")), 0);
        aiReleaseImport(scene);
    }

    // Step 2: Perform post-processing in Blender
    Command::new("blender")
        //.arg("-b")
        .arg("-P")
        .arg("postprocess.py")
        .arg("--")
        .arg(&args[1].clone().replace(".3ds", ".glb"))
        .spawn()
        .unwrap()
        .wait()
        .unwrap();
}
