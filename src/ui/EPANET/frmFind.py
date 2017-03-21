from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from ui.help import HelpHandler
from frmFindDesigner import Ui_frmFind


class frmFind(QtGui.QMainWindow, Ui_frmFind):

    def __init__(self, session, project):
        QtGui.QMainWindow.__init__(self, session)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Finding_.htm"
        self.setupUi(self)
        self.session = session
        self.project = project
        self.rbnNode.setChecked(True)
        self.gbxAdjacent.setTitle("Adjacent Links")
        QtCore.QObject.connect(self.rbnNode, QtCore.SIGNAL("clicked()"), self.rbn_Clicked)
        QtCore.QObject.connect(self.rbnLink, QtCore.SIGNAL("clicked()"), self.rbn_Clicked)
        QtCore.QObject.connect(self.rbnSources, QtCore.SIGNAL("clicked()"), self.rbn_Clicked)
        QtCore.QObject.connect(self.cmdFind, QtCore.SIGNAL("clicked()"), self.cmdFind_Clicked)

    def rbn_Clicked(self):
        if self.rbnNode.isChecked():
            self.txtID.setText("")
            self.lstAdjacent.clear()
            self.txtID.setEnabled(True)
            self.gbxAdjacent.setTitle("Adjacent Links")
        elif self.rbnLink.isChecked():
            self.txtID.setText("")
            self.lstAdjacent.clear()
            self.txtID.setEnabled(True)
            self.gbxAdjacent.setTitle("Adjacent Nodes")
        elif self.rbnSources.isChecked():
            self.txtID.setText("")
            self.lstAdjacent.clear()
            self.txtID.setEnabled(True)
            self.gbxAdjacent.setTitle("Source Nodes")

    def cmdFind_Clicked(self):
        TXT_NO_SUCH_OBJECT = 'There is no such object on the map'
        TXT_NO_SOURCE_NODES = 'There are no WQ source nodes.'
        TXT_LINK_NOT_ON_MAP = 'Link exists but is not on the map.'
        TXT_NODE_NOT_ON_MAP = 'Node exists but is not on the map.'

#         // Place map in Selection mode
#     MainForm.SelectorButtonClick;
#
# // Search database for specified node/link ID
# // and save object type and index if found.
#   s := Edit1.Text;
#   ListBox1.Clear;
#   if (RadioGroup1.ItemIndex = 2) then
#   begin
#     GetWQSources;
#     Exit;
#   end;
#   if (RadioGroup1.ItemIndex = 0) then
#     Found := Uinput.FindNode(s,FoundObject,FoundIndex)
#   else
#     Found := Uinput.FindLink(s,FoundObject,FoundIndex);
#
# // If ID found then highlight object on the map and
# // make it the current item shown in the Browser.
#   if Found then
#   begin
#     GetAdjacentObjects;
#     UpdateMapDisplay;
#     BrowserForm.UpdateBrowser(FoundObject,FoundIndex)
#   end
#
# // If not found then issue a message.
#   else
#     MessageDlg(TXT_NO_SUCH_OBJECT,mtInformation,[mbOK],0);
#   Edit1.SetFocus;
#   Edit1.SelectAll;
# end;
#
# procedure TFindForm.GetAdjacentObjects;
# //----------------------------------------------
# // Lists links connected to a found node or
# // nodes connected to a found link.
# //----------------------------------------------
# var
#   aLink: TLink;
#   aNode: TNode;
#   k,m  : Integer;
# begin
#   if FoundObject in [PIPES, PUMPS, VALVES] then
#   begin
#     aLink := Link(FoundObject,FoundIndex);
#     ListBox1.Items.Add(aLink.Node1.ID);
#     ListBox1.Items.Add(aLink.Node2.ID);
#   end
#   else
#   begin
#     aNode := Node(FoundObject,FoundIndex);
#     for k := PIPES to VALVES do
#     begin
#       for m := Network.Lists[k].Count-1 downto 0 do
#       begin
#         aLink := Link(k,m);
#         if (aLink.Node1 = aNode) or (aLink.Node2 = aNode)
#           then ListBox1.Items.Add(GetID(k,m));
#       end;
#     end;
#   end;
# end;
#
# procedure TFindForm.GetWQSources;
# //----------------------------------------------
# // Lists WQ source nodes in network
# //----------------------------------------------
# var
#   i,j,k: Integer;
#   x    : Single;
# begin
#   for i := JUNCS to TANKS do
#   begin
#     case i of
#       JUNCS:   k := JUNC_SRCQUAL_INDEX;
#       RESERVS: k := RES_SRCQUAL_INDEX;
#       TANKS:   k := TANK_SRCQUAL_INDEX;
#       else     k := 0;
#     end;
#     for j := 0 to Network.Lists[i].Count-1 do
#       if Uutils.GetSingle(Node(i,j).Data[k],x) and (x > 0) then
#         ListBox1.Items.Add(GetID(i,j));
#   end;
#   if ListBox1.Items.Count = 0 then
#     MessageDlg(TXT_NO_SOURCE_NODES,mtInformation,[mbOK],0);
# end;
#
# procedure TFindForm.UpdateMapDisplay;
# //----------------------------------------------
# // Highlights found object on the network map,
# // panning the map into position if necessary.
# //----------------------------------------------
# var
#   P1, P2, P: TPoint;
#   Xf, Yf   : Single;
#   aNode1   : TNode;
#   aNode2   : TNode;
#
# begin
#   with MapForm do
#   begin
#
#   // If found object is a link then get coords. of midpoint
#     if FoundObject in [PIPES..VALVES] then
#     begin
#       aNode1 := Link(FoundObject,FoundIndex).Node1;
#       aNode2 := Link(FoundObject,FoundIndex).Node2;
#       if not (Map.GetNodePixPos(aNode1,P1))
#       or not (Map.GetNodePixPos(aNode2,P2)) then
#       begin
#         MessageDlg(TXT_LINK_NOT_ON_MAP, mtInformation, [mbOK], 0);
#         Exit;
#       end;
#       P.X := (P1.X + P2.X) div 2;
#       P.Y := (P1.Y + P2.Y) div 2;
#       Xf := (aNode1.X + aNode2.X) / 2;
#       Yf := (aNode1.Y + aNode2.Y) / 2;
#     end
#
#   // Otherwise get found node's coords.
#     else
#     begin
#       aNode1 := Node(FoundObject,FoundIndex);
#       if not Map.GetNodePixPos(aNode1,P) then
#       begin
#         MessageDlg(TXT_NODE_NOT_ON_MAP, mtInformation, [mbOK], 0);
#         Exit;
#       end;
#       Xf := aNode1.X;
#       Yf := aNode1.Y;
#     end;
#
#   // If object within current map view window then exit
#     if PtInRect(Map.Window.MapRect,P) then Exit;
#
#   // Adjust map offset to position object in center of map
#     with Map.Window do
#     begin
#       Woffset.X := Xf - Pwidth/PPW/2;
#       Woffset.Y := Yf - Pheight/PPW/2;
#     end;
#
#   // Redraw the map
# {*** Updated 11/19/01 ***}
#     Map.RedrawBackdrop;
#     RedrawMap;
#     OVMapForm.ShowMapExtent;
#   end;
# end;
#
# procedure TFindForm.ListBox1Click(Sender: TObject);
# //---------------------------------------------------------------
# // OnClick handler for listbox that displays adjacent links/nodes
# // to the found node/link. Highlights the selected object both on
# // the map and in the Data Browser.
# //---------------------------------------------------------------
# var
#   s: String;
#   Found: Boolean;
# begin
# // Get ID of adjacent object selected
#   with ListBox1 do
#     s := Items[ItemIndex];
#
# // Search for object in Node or Link database
#   if (RadioGroup1.ItemIndex in [1,2]) then
#     Found := Uinput.FindNode(s,FoundObject,FoundIndex)
#   else
#     Found := Uinput.FindLink(s,FoundObject,FoundIndex);
#
# // If object found then highlight it on the map and
# // make it the current item shown in the Browser.
#   if Found then
#   begin
#     UpdateMapDisplay;
#     BrowserForm.UpdateBrowser(FoundObject,FoundIndex)
#   end;
# end;