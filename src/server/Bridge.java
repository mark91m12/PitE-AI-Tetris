package server;

import java.io.IOException;


import it.unical.mat.wrapper.DLVInvocationException;
import py4j.GatewayServer;

public class Bridge {

    private DlvAI dlv;

    public Bridge() {
    	try {
			dlv = new DlvAI();
		} catch (DLVInvocationException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
  
    public DlvAI getData(){
    	return dlv;
    }
    
    public static void main(String[] args) {
    	GatewayServer gatewayServer = new GatewayServer(new Bridge(), 25335);
        gatewayServer.start();
        System.out.println("Server Started");
    }

}