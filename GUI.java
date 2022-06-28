import javax.swing.*;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.BorderFactory;
import java.awt.GridLayout;
import java.awt.BorderLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Dimension;
import javax.swing.JTextField;

public class GUI implements ActionListener
{
    
    JLabel label; 
    JFrame frame;
    JPanel panel;
    JTextField textField;
    int count = 0;
    
    public GUI()
    {
        frame = new JFrame();

        JButton button = new JButton("Calculate");
        textField  = new JTextField(10);
        button.addActionListener(this);
        button.setBounds(100,100,100,50);
        textField.setPreferredSize(new Dimension(200,40));
        label = new JLabel("Input the number of fit survivors (has use of both arms and can stand upright):");
        
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setPreferredSize(new Dimension(500, 500));
        frame.setTitle("Our GUI");
        JPanel panel = new JPanel();
        panel.add(label);
        panel.add(textField);
        panel.add(button);
        frame.add(panel);
        frame.pack();
        frame.setVisible(true);
    }
    
    public static void main(String[] args)
    {
        new GUI();
    }
    
    @Override
    public void actionPerformed (ActionEvent e){
        count++;
        textField.setText("");
        if (count==1){
            label.setText("Input the number of unfit survivors:");
        } else if (count == 2){
            label.setText("Input the number of chlorate candles:");
        } else if (count == 3){
            label.setText("Input the number of ExtendAir kits:");
        } else if (count == 4){
            label.setText("Input the pressure (in fsw):");
        } else if (count == 5){
            label.setText("Input the percentage of the compartment that is flooded:");
        } else if (count == 6){
            label.setText("Input the temperature (in Fahrenheit):");
        } else if (count == 7){
            label.setText("Input the initial concentration (in %SEV) of oxygen:");
        }else if (count == 8){
            label.setText("Input the initial concentration (in %SEV) of carbon dioxide:");
        } else {
            label.setText("Start Escape Times:");
        }
    }
}
