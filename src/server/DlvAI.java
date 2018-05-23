package server;


/*
 *  Artificial Intelligence with DLV system 
 *  Authors Marco Amato Mario Egidio Carricato
 */

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import it.unical.mat.wrapper.DLVInputProgram;
import it.unical.mat.wrapper.DLVInputProgramImpl;
import it.unical.mat.wrapper.DLVInvocation;
import it.unical.mat.wrapper.DLVInvocationException;
import it.unical.mat.wrapper.DLVWrapper;
import it.unical.mat.wrapper.Model;
import it.unical.mat.wrapper.ModelBufferedHandler;
import it.unical.mat.wrapper.Predicate;
 
public class DlvAI {
 
	// path of dlv executable and files.dl

	private String dlv_path = "AI/dlv.exe";
	private String rules_path = "AI/AI.dl";
	private String config_path = "AI/config.dl";
	private String input_path = "AI/input.dl";
	
	private DLVInputProgram inputProgram;
	private Predicate result;
	
	DLVInvocation invocation = DLVWrapper.getInstance().createInvocation(dlv_path);
	ModelBufferedHandler modelBufferedHandler; 
	  
	public DlvAI() throws DLVInvocationException, IOException
	{
		inputProgram = new DLVInputProgramImpl();
		modelBufferedHandler = new ModelBufferedHandler(invocation);
	}

	public void runAI() throws DLVInvocationException, IOException{
		
		invocation.run();
 
		while (modelBufferedHandler.hasMoreModels()) // waits while DLV outputs a new model
		{
			Model model = modelBufferedHandler.nextModel();
			
			for (int i = 0; i< model.size(); i++) {
 
				Predicate temp = model.getPredicate(i);
				
				//System.out.println("result => "+temp);
 				setResult(temp);
			}
 		}		
		invocation.reset();
	}

	public Predicate getResult() {
		return result;
	}

	public void setResult(Predicate p) {
		this.result = p;
	}
	
	public int getX(){
		return Integer.parseInt(result.getTermAt(0,2));
	}
	
	public int getY(){
		return Integer.parseInt(result.getTermAt(0, 1));
	}
	
	public int getRotation(){
		return Integer.parseInt(result.getTermAt(0, 3));
	}
	
	public void reset() throws DLVInvocationException{
		inputProgram.clean();
		
		inputProgram.addFile(rules_path);
		inputProgram.addFile(config_path);
		inputProgram.addFile(input_path);

		invocation.setNumberOfModels(1);
 		
 		List<String> filters=new ArrayList<String>();
 		filters.add("place");
 		invocation.setFilter(filters, true);
 		
		invocation.setInputProgram(inputProgram);
	}
	
}