while [ ! -f HSC.pkl ] ; do
  echo "Single-sequence predictor model not found."
  read -p "[1]Download [2]Generate in-house: " yn
  case $yn in
    [1]* )  wget -O HSC.pkl "https://studki-my.sharepoint.com/personal/dimitri_wirjowerdojo_stud_ki_se/_layouts/15/guestaccess.aspx?docid=19b17f73483f84d0eb5f6aeee594f529d&authkey=AdDN3w20mDcqh3qSIKmzyO8" -q --show-progres ;;
    [2]* ) cd bin ; python HSC_Model_Generator.py ; cd .. ;;
    * ) echo "Please input '1' to Download or '2' to generate locally." ;;
  esac
done

while [ ! -f FM.pkl ] ; do
  echo "PSSM-Frequency Matrix-based predictor model not found."
  read -p "[1]Download [2]Generate in-house: " yn
  case $yn in
    [1]* ) wget -O FM.pkl "https://studki-my.sharepoint.com/personal/dimitri_wirjowerdojo_stud_ki_se/_layouts/15/guestaccess.aspx?docid=0593b2b0d6b3e4b818d735390cef84ccb&authkey=ATCodfV9L6G0tBmrUCRnSY8" -q --show-progress ;;
    [2]* ) cd bin ; python FM_Model_Generator.py ; cd .. ;;
    * ) echo "Please input '1' to Download or '2' to generate locally." ;;
  esac
done

while [ ! -f SM.pkl ] ; do
  echo "PSSM-Substitution Matrix-based predictor model not found."
  read -p "[1]Download [2]Generate in-house: " yn
  case $yn in
    [1]* ) wget -O SM.pkl "https://studki-my.sharepoint.com/personal/dimitri_wirjowerdojo_stud_ki_se/_layouts/15/guestaccess.aspx?docid=04390ce8c450b48a5ab9df1e426186f46&authkey=AVxwcWHd-JUPrJtgd90xdPg" -q --show-progress ;;
    [2]* ) cd bin ; python SM_Model_Generator.py ; cd .. ;;
    * ) echo "Please input '1' to Download or '2' to generate locally." ;;
  esac
done

echo "Models exist.
"
